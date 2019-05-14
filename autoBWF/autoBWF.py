import sys
import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from autoBWF.tabbed import Ui_autoBWF
from autoBWF.BWFfileIO import call_bwf, get_bwf_core, get_bwf_tech, get_xmp, set_xmp
from autoBWF.autobwfconfig import default_config


class MainWindow(QtWidgets.QMainWindow, Ui_autoBWF):
    def __init__(self, filename, config, template, parent=None):
        self.autobwf_ns = "http://ns.ukrhec.org/autoBWF/0.1"

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.config = config

        self.gui_text_widgets = {
                                  "Description": self.descriptionLine,
                                  "Originator": self.originatorLine,
                                  "OriginationDate": self.originationDateLine,
                                  "OriginationTime": self.originationTimeLine,
                                  "OriginatorReference": self.originatorRefLine,
                                  "CodingHistory": self.codingHistoryText,
                                  "INAM": self.titleLine,
                                  "ICRD": self.creationDateLine,
                                  "ITCH": self.technicianBox,
                                  "ISFT": self.isftSelect,
                                  "ISRC": self.sourceSelect,
                                  "ICMT": self.commentText,
                                  "ICOP": self.copyrightText,
                                  "description": self.descriptionText,  # TODO terrible choice of key...
                                  "owner": self.rightsOwnerSelect,
                                  "language": self.languageLine,
                                  "interviewer": self.interviewerLine,
                                  "interviewee": self.intervieweeLine
                                 }
        self.xmp_fields = ("description", "owner", "language", "interviewer", "interviewee")

        self.filename = filename
        self.original_md = {}
        self.template_md = {}

        self.base_command = ["bwfmetaedit", "--specialchars"]
        if config["accept-nopadding"]:
            self.base_command.append("--accept-nopadding")

        #
        # configure dropdowns and texts
        #

        self.originatorLine.insert(config["originator"])
        self.speedSelect.addItems(config["speed"])
        self.mediaSelect.addItems(config["media"])
        self.eqSelect.addItems(config["eq"])
        self.typeSelect.addItems(config["type"])
        self.technicianBox.addItems(config["technician"])
        self.isftSelect.addItems(config["isft"])
        self.sourceSelect.addItems(config["source"])
        self.rightsOwnerSelect.addItems(config["owner"])
        self.deckSelect.addItems(config["deck"]["list"])
        self.adcSelect.addItems(config["adc"]["list"])
        self.softwareSelect.addItems(config["software"]["list"])
        self.copyrightSelect.addItems(config["copyright"]["list"])
        self.copyrightText.insertPlainText(
            config["copyright"][config["copyright"]["list"][0]]
        )

        #
        # set up signals/slots
        #

        self.copyrightSelect.activated.connect(self.copyright_activated)
        self.deckSelect.currentIndexChanged.connect(self.update_coding_history)
        self.adcSelect.currentIndexChanged.connect(self.update_coding_history)
        self.softwareSelect.currentIndexChanged.connect(self.update_coding_history)
        self.mediaSelect.currentIndexChanged.connect(self.update_coding_history)
        self.speedSelect.currentIndexChanged.connect(self.update_coding_history)
        self.eqSelect.currentIndexChanged.connect(self.update_coding_history)
        self.typeSelect.currentIndexChanged.connect(self.update_coding_history)
        self.actionUpdate_metadata.triggered.connect(self.save_metadata)
        self.actionQuit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionOpen_template.triggered.connect(self.open_template)

        self.tabWidget.setEnabled(False)
        self.actionUpdate_metadata.setEnabled(False)
        self.actionOpen_template.setEnabled(False)

        if filename:
            self.tabWidget.setEnabled(True)
            self.actionUpdate_metadata.setEnabled(True)
            self.actionOpen.setEnabled(False)

            md = get_bwf_tech(config["accept-nopadding"], filename)
            if md["Errors"] != "":
                print(filename + " does not appear to be a valid Wave file")
            else:
                self.original_md.update(md)
            self.populate_file_info(filename)

        if template:
            self.populate_template_info(template)

    @staticmethod
    def activate_changed(input_widget):
        input_widget.setStyleSheet("color: red; font: normal")

    def get_gui_text(self, widget_name):
        widget = self.gui_text_widgets[widget_name]
        widget_type = type(widget)
        if widget_type is QtWidgets.QPlainTextEdit:
            return widget.toPlainText()
        if widget_type is QtWidgets.QLineEdit:
            return widget.text()
        if widget_type is QtWidgets.QComboBox:
            return widget.currentText()
        return None

    def get_all_gui_texts(self):
        md = {}
        for field in self.gui_text_widgets.keys():
            md[field] = self.get_gui_text(field)
        return md

    def set_gui_text(self, widget_name, value, is_original_md=False):
        widget = self.gui_text_widgets[widget_name]
        widget_type = type(widget)
        if widget_type is QtWidgets.QPlainTextEdit:
            widget.clear()
            widget.insertPlainText(value)
        if widget_type is QtWidgets.QLineEdit:
            widget.clear()
            widget.insert(value)
        if widget_type is QtWidgets.QComboBox:
            widget.setCurrentText(value)

        if is_original_md:
            widget.setStyleSheet("color: grey; font: italic")
            if widget_type is QtWidgets.QComboBox:
                widget.currentTextChanged.connect(lambda: self.activate_changed(widget))
            else:
                widget.textChanged.connect(lambda: self.activate_changed(widget))

    def open_file(self):
        fname = str(QFileDialog.getOpenFileName(self, "Open Wave file", "~")[0])
        if fname:
            # check to make sure file is legit
            md = get_bwf_tech(self.config["accept-nopadding"], fname)
            if md["Errors"] != "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(fname + " does not appear to be a valid Wave file")
                msg.exec_()
            else:
                self.original_md.update(md)
                self.filename = fname

                self.tabWidget.setEnabled(True)
                self.actionUpdate_metadata.setEnabled(True)
                self.actionOpen_template.setEnabled(True)
                self.actionOpen.setEnabled(False)
                self.populate_file_info(fname)

    def open_template(self):
        fname = str(QFileDialog.getOpenFileName(self, "Open template file", "~")[0])
        if fname:
            # check to make sure file is legit
            md = get_bwf_tech(self.config["accept-nopadding"], fname)
            if md["Errors"] != "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(fname + " does not appear to be a valid Wave file")
                msg.exec_()
            else:
                self.actionOpen_template.setEnabled(False)
                self.populate_template_info(fname)

    def set_existing(self, name):
        if self.original_md[name] != "" and (self.original_md[name] is not None):
            self.set_gui_text(name, self.original_md[name], is_original_md=True)

    def populate_file_info(self, file):
        import re
        import os.path
        from datetime import datetime

        date_time_created = datetime \
            .fromtimestamp(os.path.getctime(file)) \
            .replace(microsecond=0) \
            .isoformat()
        [date_created, time] = date_time_created.split("T")

        m = re.compile(self.config["filenameRegex"]).match(file)
        if m:
            matches = m.groups()
            identifier = matches[0]
            identifier = identifier.replace("-", ".")
            identifier = identifier.replace("_", "")

            file_use = matches[1]
            date_from_filename = matches[2]
            date_from_filename = (
                    date_from_filename[0:4] + "-" +
                    date_from_filename[4:6] + "-" +
                    date_from_filename[6:]
            )

            if date_created != date_from_filename:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Filename and timestamp dates disagree")
                msg.setInformativeText(
                    "filename: " + date_from_filename +
                    "\ntimestamp: " + date_created)
                msg.setWindowTitle("Choose date")
                msg.addButton('Use ' + date_from_filename, QMessageBox.NoRole)
                msg.addButton('Use ' + date_created, QMessageBox.YesRole)
                retval = msg.exec_()
                if retval == 1:
                    date_from_filename = date_created

            self.set_gui_text("OriginationDate", date_from_filename)
            self.set_gui_text("OriginationTime", time)
            self.set_gui_text("OriginatorReference",
                              self.config["repocode"] + " " +
                              date_from_filename.replace("-", "") + " " +
                              time.replace(":", ""))

            try:
                file_use = self.config["fileuse"][file_use]
            except KeyError:
                # TODO: make this a dialog
                print(
                    file_use +
                    " does not not have a standard translation"
                )
                file_use = "Unknown"

            description = (
                "File content: " + identifier +
                "; File use: " + file_use +
                "; Original filename: " + os.path.basename(file)
            )
            self.set_gui_text("Description", description)
        else:
            QMessageBox.warning(
                self, 'Warning',
                file + " does not follow file naming convention"
            )
            self.set_gui_text("OriginationDate", date_created)
            self.set_gui_text("OriginationTime", time)
            self.set_gui_text("OriginatorReference",
                              self.config["repocode"] + " " +
                              date_created.replace("-", "") + " " +
                              time.replace(":", ""))

        self.update_coding_history()

        #
        # prefill defaults and insert existing values
        #

        self.original_md.update(get_bwf_core(self.config["accept-nopadding"], file))
        self.original_md.update(get_xmp(file, self.base_command))

        fields_to_fill = ["Description", "Originator", "OriginationDate",
                          "OriginationTime", "OriginatorReference", "CodingHistory",
                          "INAM", "ICMT", "ICRD", "ITCH", "ISFT", "ISRC", "ICOP",
                          "description", "owner", "language", "interviewer", "interviewee"]
        for field in fields_to_fill:
            self.set_existing(field)

        if self.original_md["MD5Stored"] != "":
            self.md5Check.setEnabled(False)

    def set_value_from_template(self, name):
        if self.template_md[name] != "":
            self.set_gui_text(name, self.template_md[name])

    def populate_template_info(self, file):
        # replace with template values if they exist

        if file is not None:
            self.template_md.update(get_bwf_core(self.config["accept-nopadding"], file))
            self.template_md.update(get_xmp(file, self.base_command))

            fields_to_fill = ["CodingHistory", "INAM", "ICRD", "ITCH", "ISRC", "ICOP",
                              "description", "owner", "language", "interviewer", "interviewee"]
            for field in fields_to_fill:
                self.set_value_from_template(field)

    def copyright_activated(self, index):
        self.set_gui_text("ICOP", self.config["copyright"][self.config["copyright"]["list"][index]])

    def update_coding_history(self):
        deck = self.deckSelect.currentText()
        adc = self.adcSelect.currentText()
        software = self.softwareSelect.currentText()
        media = self.mediaSelect.currentText()
        speed = self.speedSelect.currentText()
        eq = self.eqSelect.currentText()
        type = self.typeSelect.currentText()

        analogprops = [x for x in [self.config["deck"][deck], media, speed, eq, type] if x != ""]
        channels = {"1": "mono", "2": "stereo"}

        history_list = [
            "A=ANALOGUE,M=stereo,T=", "; ".join(analogprops),
            "\r\nA=PCM,F=", self.original_md["SampleRate"],
            ",W=", self.original_md["BitPerSample"],
            ",M=stereo,T=", self.config["adc"][adc],
            "\r\nA=PCM,F=", self.original_md["SampleRate"],
            ",W=" + self.original_md["BitPerSample"],
            ",M=" + channels[self.original_md["Channels"]],
            ",T=" + self.config["software"][software]
        ]
        self.set_gui_text("CodingHistory", "".join(history_list))

    def save_metadata(self):
        current_md = self.get_all_gui_texts()
        changed_xmp = {k: current_md[k] for k in self.xmp_fields if current_md[k] != self.original_md[k]}
        current_xmp = {k: current_md[k] for k in self.xmp_fields}
        changed_bwf_riff = {k: current_md[k] for k in current_md.keys()
                            if k not in self.xmp_fields and current_md[k] != self.original_md[k]}

        if not changed_xmp and not changed_bwf_riff:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Metadata is unchanged. Nothing to update.")
            msg.exec_()
            return

        if self.md5Check.isChecked() and self.md5Check.isEnabled():
            command = self.base_command
            command.extend(["--MD5-embed", self.filename])
            subprocess.run(command)

        if self.original_md["TimeReference"] != '0':
            call_bwf(self.base_command, self.filename, "TimeReference", "0")

        # need to save coding history for last.
        # If we don't, then for some bizarre reason
        # there's duplication of the last two characters of the history string...
        coding_history = changed_bwf_riff.pop("CodingHistory", None)

        for key in changed_bwf_riff:
            call_bwf(self.base_command, self.filename, key, current_md[key])

        if coding_history:
            call_bwf(self.base_command, self.filename, "CodingHistory", coding_history)

        # something has changed, therefore at minimum we need to update xmp:MetadataDate
        set_xmp(current_xmp, self.filename, self.base_command)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Metadata saved successfully")
        # TODO what if it wasn't successful???
        msg.exec_()


def main():
    import json
    import argparse
    from pathlib import Path

    from appdirs import AppDirs

    try:
        subprocess.check_output("bwfmetaedit")
    except FileNotFoundError:
        exit((
            "You must have the BWFMetaEdit CLI installed on your system to run autoBWF.\n"
            "Please download and install the latest version from https://mediaarea.net/BWFMetaEdit/Download.\n"
            "Note that you must install the 'CLI' interface."))

    default_text = default_config()

    dirs = AppDirs("autoBWF", "UHEC")
    config_file = Path(dirs.user_data_dir) / "autobwfconfig.json"

    try:
        config_text = config_file.read_text()
    except FileNotFoundError:
        Path(dirs.user_data_dir).mkdir(parents=True, exist_ok=True)
        config_handle = config_file.write_text(default_text)
        config_text = default_text

    config = json.loads(config_text)

    parser = argparse.ArgumentParser(description='Create internal metadata for WAV file(s).')
    parser.add_argument('filename', nargs='?', help='WAV file to be processed')
    parser.add_argument('-t', help="template file")
    args = parser.parse_args()
    filename = args.filename
    template = args.t

    if filename:
        # check to make sure file is legit
        techMD = get_bwf_tech(config["accept-nopadding"], filename)
        if techMD["Errors"] != "":
            print(filename + " does not appear to be a valid Wave file")
            sys.exit(1)

    if template:
        # check to make sure file is legit
        dum = get_bwf_tech(config["accept-nopadding"], template)
        if dum["Errors"] != "":
            print(template + " does not appear to be a valid Wave file")
            sys.exit(1)

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow(filename, config, template)
    form.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
