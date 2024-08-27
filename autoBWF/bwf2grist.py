import sys
from os import path
import subprocess
import logging
from logging.config import dictConfig
from datetime import datetime, timezone

import click
import requests

from autoBWF.BWFfileIO import get_bwf_tech
from autoBWF.BWFfileIO import get_bwf_core


@click.command()
@click.option('--key', envvar='GRIST_KEY', help="provide Grist API key")
@click.option('--digest', is_flag=True, help="verify MD5 digest of data chunk (may be very slow)")
@click.option('-y', '--yes', is_flag=True, help="Assume 'yes' as answer to all prompts")
@click.option('--dry-run', is_flag=True,
              help="Simulate Grist actions, but don't actually make changes in Grist")
@click.option('-q', '--quiet', is_flag=True, help='turn off logging to stderr')
@click.argument('files', nargs=-1)
def cli(key, digest, yes, dry_run, quiet, files):
    """
    bwf2grist is a tool to interact with the Grist (getgrist.com) API to create, update, or validated rows(s) in a
    table of PBCore Digital Instantiations based on a BWF file.
    """

    logging_config = dict(
        version=1,
        formatters={
            'verbose': {
                'format': "%(asctime)s %(name)-12s %(levelname)-8s [%(filename)s:%(funcName)20s] %(message)s"
            },
            'full': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        handlers={
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': logging.DEBUG
            }
        },
        root={
            'level': logging.DEBUG,
        }
    )

    handler_list = []

    if not quiet:
        handler_list.append('console')

    logging_config['root']['handlers'] = handler_list

    dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    field_mapping = {"OriginalFilename": "Digital_instantiation_identifier", "FileUse": "FileUse",
                     "Duration": "Duration",
                     "ICMT": "Digitization_comment", "MD5Stored": "MD5Stored", "OriginationDate": "OriginationDate",
                     "OriginationTime": "OriginationTime", "CodingHistory": "CodingHistory", "ITCH": "Technician",
                     "ISFT": "Creating_software", "Channels": "Channels", "SampleRate": "SampleRate",
                     "BitPerSample": "BitPerSample"}

    base_url = "https://docs.getgrist.com/api"
    tables_base_url = f"{base_url}/docs/mjNHbyaMvvvbRET8NRN6Pf/tables"
    headers = {"Authorization": f"Bearer {key}"}

    for infile in files:
        try:
            metadata = get_bwf_core(infile)
            metadata["filename"] = infile
            if digest:
                metadata.update(get_bwf_tech(infile, verify_digest=True))
                if metadata["MD5Stored"] != metadata["MD5Calculated"]:
                    logger.error('Calculated and stored MD5 digests for %s do not match', infile)
                    continue
            else:
                metadata.update(get_bwf_tech(infile))
        except subprocess.CalledProcessError:
            continue

        if metadata["filename"] != metadata["OriginalFilename"]:
            logger.warning('Current (%s) and original (%s) filenames do not match',
                           infile, metadata["OriginalFilename"])

        identifier = metadata["OriginalFilename"]

        # remap BWFfileIO field names to Grist field names, and get rid of the unused ones
        metadata = {field_mapping[k]: metadata[k] for k in metadata.keys() if k in field_mapping.keys()}

        grist_records = requests.get(f"{tables_base_url}/Digital_instantiations/records", headers=headers,
                                     params={"filter": f'{{"Digital_instantiation_identifier": ["{identifier}"]}}'})
        records = grist_records.json()["records"]

        # convert the OriginationDate from ISO to unix timestamp to match how Grist encodes dates
        if metadata["OriginationDate"] != "":
            date_obj = datetime.strptime(metadata["OriginationDate"], '%Y-%m-%d')
            date_obj = date_obj.replace(tzinfo=timezone.utc)
            metadata["OriginationDate"] = int(date_obj.timestamp())

        # convert the fields which are integers in Grist into integers
        metadata["Channels"] = int(metadata["Channels"])
        metadata["SampleRate"] = int(metadata["SampleRate"])
        metadata["BitPerSample"] = int(metadata["BitPerSample"])

        if len(records) == 0:
            logger.debug("creating new digital instantiation %s", identifier)
            grist_out = requests.post(f"{tables_base_url}/Digital_instantiations/records", headers=headers,
                                      json={"records": [{"fields": metadata}]})

            if grist_out.status_code == requests.codes.ok:
                logger.info("digital instantiation %s successfully created", identifier)
            elif grist_out.ok:
                logger.warning("digital instantiation creation returned a status > 200 but < 400")
            else:
                logger.error("digital instantiation %s could not be created", identifier)
        elif len(records) > 1:
            message = ("the identifier %s has more than one digital instantiation record in Grist"
                       " -- this isn't supposed to happen")
            logger.error(message, identifier)
            continue
        else:
            grist_data = records[0]['fields']
            row_id = records[0]['id']
            logger.debug("updating digital instantiation %s, record id %d", identifier, row_id)

            differences = {k: metadata[k] for k in metadata.keys()
                           if metadata[k] != "" and grist_data[k] and metadata[k] != grist_data[k]}

            new_fields = {k: metadata[k] for k in metadata.keys()
                          if metadata[k] != "" and (grist_data[k] == "" or grist_data[k] is None)}

            if new_fields:
                print("the BWF file has the following fields that are not in Grist:")
                pretty_print(new_fields)
                if click.confirm('Do you want to update the metadata in Grist?'):
                    grist_out = requests.patch(f"{tables_base_url}/Digital_instantiations/records", headers=headers,
                                               json={"records": [{"id": row_id, "fields": new_fields}]})

                    if grist_out.status_code == requests.codes.ok:
                        logger.info("digital instantiation %s successfully updated", identifier)
                    elif grist_out.ok:
                        logger.warning("digital instantiation update returned a status > 200 but < 400")
                    else:
                        logger.error("digital instantiation %s could not be updated", identifier)

            if differences:
                print("the following fields in the BWF file differ from those in Grist:")
                pretty_print(differences)
                if click.confirm('Do you want to update the metadata in Grist?'):
                    grist_out = requests.patch(f"{tables_base_url}/Digital_instantiations/records", headers=headers,
                                               json={"records": [{"id": row_id, "fields": differences}]})

                    if grist_out.status_code == requests.codes.ok:
                        logger.info("digital instantiation %s successfully updated", identifier)
                    elif grist_out.ok:
                        logger.warning("digital instantiation update returned a status > 200 but < 400")
                    else:
                        logger.error("digital instantiation %s could not be updated", identifier)

            if not new_fields and not differences:
                print("the metadata in the BWF file match those in Grist")


def pretty_print(thing):
    for name, val in thing.items():
        print(f'{name:20} => {val}')


if __name__ == '__main__':
    cli()
