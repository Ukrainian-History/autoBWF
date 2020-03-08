"""An opinionated alternative GUI for FADGI BWFMetaEdit.

The purpose of autoBWF is to provide an alternative GUI for embedding internal metadata in WAVE audio files
using the Broadcast Wave standard, FADGI BWFMetaEdit, and XMP. Unlike the existing BWFMetaEdit GUI, autoBWF is
extremely opinionated and will automatically generate metadata content based on file naming conventions,
system metadata, and pre-configured repository defaults. In addition, it can copy metadata fields from a template
file to avoid having to enter the same information multiple times for several master or derivative files of the same
physical instantiation.

"""

import sys
import subprocess
import time
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5 import QtCore

from autoBWF.tabbed import Ui_autoBWF
from autoBWF.export_dialog import Ui_Export
import autoBWF.BWFfileIO as bwfio
from autoBWF.autobwfconfig import default_config


class MainWindow(QtWidgets.QMainWindow, Ui_autoBWF):
    """The main PyQt GUI window.

    All metadata fields are indentified by a standard identifier. The values of these fields are stored in dicts,
    and the text and switcher menu widgets associated with each field are also stored in dicts indexed by the
    same identifiers.
    """

    def __init__(self, filename, config, template):
        """Main window __init__ method.

        Configures PyQt widgets, sets up signals/slots, and loads any files specified on the command line.

        Args:
            filename (str): Name of target Wave file specified on the command line.
            config (dict): Parsed contents of the configuration file.
            template (str): Name of template BWF file specified on the command line.

        """
        super(MainWindow, self).__init__(None)
        self.setupUi(self)

        self.config = config
        self.filename = filename
        self.original_md = {}  #: Embedded metadata already present in the target file
        self.template_md = None  #: Embedded metadata present in the template file
        self.edited_md = {}  #: Metadata values that have been edited by the GUI user.

        if config["accept-nopadding"]:
            bwfio.bwfmetaedit.append("--accept-nopadding")

        #: dict of PyQt widgets: all text input widgets in the GUI, indexed by metadata field name
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
            "IARL": self.iarlLine,
            "xmp_description": self.XMPdescriptionText,
            "owner": self.rightsOwnerSelect,
            "language": self.languageLine,
            "interviewer": self.interviewerLine,
            "interviewee": self.intervieweeLine,
            "form": self.formSelect,
            "host": self.hostLine,
            "speaker": self.speakerLine,
            "performer": self.performerLine,
            "topics": self.topicsLine,
            "names": self.namesLine,
            "events": self.eventsLine,
            "places": self.placesLine,
            "creator": self.creatorSelect,
        }
        self.xmp_fields = ["xmp_description", "owner", "language", "interviewer", "interviewee",
                           "form", "host", "speaker", "performer", "topics", "names", "events", "places",
                           "creator"]

        #: dict of PyQt widgets: all original/edited/template toggle menus, indexed by metadata field name
        self.switchers = {
            "Description": self.descriptionSwitcher,
            "Originator": self.originatorSwitcher,
            "OriginationDate": self.originationDateSwitcher,
            "OriginationTime": self.originationTimeSwitcher,
            "OriginatorReference": self.originatorRefSwitcher,
            "CodingHistory": self.codingHistorySwitcher,
            "INAM": self.titleSwitcher,
            "ICRD": self.creationDateSwitcher,
            "ITCH": self.technicianSwitcher,
            "ISFT": self.isftSwitcher,
            "ISRC": self.sourceSwitcher,
            "ICMT": self.commentSwitcher,
            "ICOP": self.copyrightSwitcher,
            "IARL": self.iarlSwitcher,
            "xmp_description": self.XMPdescriptionSwitcher,
            "owner": self.rightsOwnerSwitcher,
            "language": self.languageSwitcher,
            "interviewer": self.interviewerSwitcher,
            "interviewee": self.intervieweeSwitcher,
            "form": self.formSwitcher,
            "host": self.hostSwitcher,
            "speaker": self.speakerSwitcher,
            "performer": self.performerSwitcher,
            "topics": self.topicsSwitcher,
            "names": self.namesSwitcher,
            "events": self.eventsSwitcher,
            "places": self.placesSwitcher,
            "creator": self.creatorSwitcher,
        }

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
        self.iarlLine.insert(config["iarl"])
        self.sourceSelect.addItems(config["source"])
        self.rightsOwnerSelect.addItems(config["owner"])
        self.deckSelect.addItems(config["deck"]["list"])
        self.adcSelect.addItems(config["adc"]["list"])
        self.softwareSelect.addItems(config["software"]["list"])
        self.copyrightSelect.addItems(config["copyright"]["list"])
        self.formSelect.addItems(config["form"])
        self.copyrightText.insertPlainText(
            config["copyright"][config["copyright"]["list"][0]]
        )
        self.creatorSelect.addItems(config["creator"])

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
        self.actionQuit.triggered.connect(self.close_window)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionOpen_template.triggered.connect(self.open_template)
        self.actionExport_metadata.triggered.connect(self.export_metadata)

        self.tabWidget.setEnabled(False)
        self.actionUpdate_metadata.setEnabled(False)
        self.actionOpen_template.setEnabled(False)
        self.actionExport_metadata.setEnabled(False)

        for switcher in self.switchers:
            self.switchers[switcher].setEnabled(False)
            for i in range(3):
                self.switchers[switcher].model().item(i).setEnabled(False)

            self.switchers[switcher].currentIndexChanged.connect(
                lambda value, widget=switcher: self.switcher_changed(widget, value)
            )

        # deal with files specified on the command line
        if filename:
            self.filepath = str(Path(filename).resolve())
            self.original_md = self.load_file(filename)
            if self.original_md is not None:
                self.tabWidget.setEnabled(True)
                self.actionUpdate_metadata.setEnabled(True)
                self.actionExport_metadata.setEnabled(True)
                self.actionOpen.setEnabled(False)
                self.populate_file_info(filename)
        if template:
            self.template_md = self.load_file(template)
            if self.template_md is not None:
                self.populate_template_info()

    @staticmethod
    def load_file(file, die_on_error=True):
        """Read metadata from a BWF file.

        Args:
            file (str): The name of the BWF file.
            die_on_error (bool): If True, then exit the GUI if file is unreadable.

        Returns:
            Dict of metadata if successful, None otherwise.

        """
        md = bwfio.check_wave(file)
        if md is not None:
            md.update(bwfio.get_bwf_core(file))
            md.update(bwfio.get_xmp(file))
            return md

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(file + " does not appear to be a valid Wave file")
        msg.exec_()

        if die_on_error:
            QtCore.QCoreApplication.quit()

        return md

    def text_changed(self, input_widget):
        """Slot function called in response to a change in the contents of a text widget.

        Args:
            input_widget (PyQt widget): The PyQt widget that experienced the text change.
        """
        text_now = self.get_gui_text(input_widget)
        if self.original_md[input_widget] != text_now:
            self.gui_text_widgets[input_widget].setStyleSheet("color: red; font: normal")
            self.edited_md[input_widget] = text_now
            self.switchers[input_widget].setEnabled(True)
            self.switchers[input_widget].model().item(0).setEnabled(True)
            self.switchers[input_widget].model().item(1).setEnabled(True)
            self.switchers[input_widget].setCurrentIndex(0)
        else:
            self.gui_text_widgets[input_widget].setStyleSheet("color: grey; font: italic")
            self.switchers[input_widget].setCurrentIndex(1)
            self.switchers[input_widget].model().item(0).setEnabled(False)
            del self.edited_md[input_widget]

    def switcher_changed(self, input_widget, value):
        """Slot function called in response to a change in an original/edited/template toggle menu.

        Args:
            input_widget (PyQt widget): The PyQt menu that experienced the change.
            value (int): The selected menu item.
        """
        if value == 0:
            self.set_text_to_edited(input_widget)
        if value == 1:
            self.set_text_to_original(input_widget)
        if value == 2:
            self.set_text_to_template(input_widget)

    def get_gui_text(self, md_field_name):
        """Extract the current text from the widget corresponding to a metadata field.

        Convenience function to deal with the fact that different widget types have different accessor methods.

        Args:
            md_field_name (str): The name of the metadata field to extract.

        Returns:
            The string contained in the text widget corresponding to the metadata field, or None if the widget
            type is unrecognized.
        """

        widget = self.gui_text_widgets[md_field_name]
        widget_type = type(widget)
        if widget_type is QtWidgets.QPlainTextEdit:
            return widget.toPlainText()
        if widget_type is QtWidgets.QLineEdit:
            return widget.text()
        if widget_type is QtWidgets.QComboBox:
            return widget.currentText()
        return None

    def get_all_gui_texts(self):
        """Extract texts from all metadata widgets.

        Returns:
            dict of metadata values.
        """
        md = {}
        for field in self.gui_text_widgets.keys():
            md[field] = self.get_gui_text(field)
        return md

    def get_current_and_changed(self):
        """Extract texts from all metadata widgets and which metadata have been changed.

        Returns:
            Tuple of three dicts, containing the current GUI metadata values, the changed BWF/RIFF values,
            and the changed XMP values, respectively.
        """

        current_md = self.get_all_gui_texts()
        changed_xmp = {k: current_md[k] for k in self.xmp_fields if current_md[k] != self.original_md[k]}
        changed_bwf_riff = {k: current_md[k] for k in current_md.keys()
                            if k not in self.xmp_fields and current_md[k] != self.original_md[k]}

        return current_md, changed_bwf_riff, changed_xmp

    def set_gui_text(self, widget_name, value, block=True):
        """Set a GUI text element to a given value.

        Args:
            widget_name (str): The name of the widget whose text is to be changed.
            value (str): The string that the contents of widget_name should be set to.
            block (bool): If True, block all signals to prevent infinte recursion.
        """
        widget = self.gui_text_widgets[widget_name]
        widget_type = type(widget)
        if block:
            widget.blockSignals(True)

        if widget_type is QtWidgets.QPlainTextEdit:
            widget.clear()
            widget.insertPlainText(value)
        if widget_type is QtWidgets.QLineEdit:
            widget.clear()
            widget.insert(value)
        if widget_type is QtWidgets.QComboBox:
            widget.setCurrentText(value)

        if block:
            widget.blockSignals(False)

    def set_text_to_original(self, widget_name):
        """Set the text in the widget corresponding to widget_name to the value in the target file."""
        text = self.original_md[widget_name]
        if text != "":
            self.set_gui_text(widget_name, text)
            self.gui_text_widgets[widget_name].setStyleSheet("color: grey; font: italic")

    def set_text_to_edited(self, widget_name):
        """Set the text in the widget corresponding to widget_name to the last edited value."""
        text = self.edited_md[widget_name]
        self.set_gui_text(widget_name, text)
        self.gui_text_widgets[widget_name].setStyleSheet("color: red; font: regular")

    def set_text_to_template(self, widget_name):
        """Set the text in the widget corresponding to widget_name to the value in the template file."""
        if self.template_md:
            text = self.template_md[widget_name]
            if text != "":
                self.set_gui_text(widget_name, text)
                if text == self.original_md[widget_name]:
                    self.gui_text_widgets[widget_name].setStyleSheet("color: grey; font: italic")
                elif self.original_md[widget_name] == "":
                    self.gui_text_widgets[widget_name].setStyleSheet("color: black; font: normal")
                else:
                    self.gui_text_widgets[widget_name].setStyleSheet("color: #F5D76E; font: italic")

    def open_file(self):
        """Slot function called in response to the "Open" menu bar action."""
        fname = str(QFileDialog.getOpenFileName(self, "Open Wave file", "~")[0])
        if fname:
            self.original_md = self.load_file(fname)
            if self.original_md is not None:
                self.filename = fname
                self.tabWidget.setEnabled(True)
                self.actionUpdate_metadata.setEnabled(True)
                self.actionExport_metadata.setEnabled(True)
                self.actionOpen_template.setEnabled(True)
                self.actionOpen.setEnabled(False)
                self.populate_file_info(fname)

    def open_template(self):
        """Slot function called in response to the "Load template" menu bar action."""
        fname = str(QFileDialog.getOpenFileName(self, "Open template file", "~")[0])
        if fname:
            self.template_md = self.load_file(fname, die_on_error=False)
            if self.template_md is not None:
                self.actionOpen_template.setEnabled(False)
                self.populate_template_info()

    def populate_file_info(self, file, reload=False):
        """Replace contents of text widgets with any pre-existing metadata in the target BWF file.

        Args:
            file (str): The name of the target file.
            reload (bool): If True, prevent date warning messagebox and block signals, which is what is desired
                if the file is being reloaded after metadata save.
        """

        import re
        import os.path
        from datetime import datetime

        #
        # Generate and pre-fill defaults
        #

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

            if date_created != date_from_filename and not reload:
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
                QMessageBox.warning(
                    self, 'Warning',
                    file_use + " does not not have a standard translation"
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
            description = ""

        self.update_coding_history(block=reload)

        #
        # insert existing values
        #

        for field in self.gui_text_widgets.keys():
            if self.original_md[field] != "":
                self.set_text_to_original(field)
                widget = self.gui_text_widgets[field]
                widget_type = type(widget)
                if widget_type is QtWidgets.QComboBox:
                    widget.currentTextChanged.connect(lambda value, element=field: self.text_changed(element))
                elif widget_type is QtWidgets.QPlainTextEdit:
                    widget.textChanged.connect(lambda element=field: self.text_changed(element))
                else:
                    widget.textEdited.connect(lambda value, element=field: self.text_changed(element))

        # check sanity of existing BWF description field
        if self.original_md["Description"] != "" and description != self.original_md["Description"]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("BWF Description is inconsistent with filename")
            msg.setInformativeText(
                              "Field will be regenerated. " +
                              "The original can be restored using the drop-down menu next to the text box."
                        )
            msg.exec_()
            self.set_gui_text("Description", description, block=False)

        if self.original_md["MD5Stored"] != "":
            self.md5Check.setEnabled(False)

    def populate_template_info(self):
        """Replace contents of selected text widgets with any pre-existing metadata in the template BWF file."""

        fields_to_fill = ["CodingHistory", "INAM", "ICRD", "ITCH", "ISRC", "ICOP", "IARL"]
        fields_to_fill.extend(self.xmp_fields)
        for field in fields_to_fill:
            if self.template_md[field] != "":
                self.set_text_to_template(field)
                if self.original_md[field] != "" and self.original_md[field] != self.template_md[field]:
                    self.switchers[field].setEnabled(True)
                    self.switchers[field].model().item(1).setEnabled(True)
                    self.switchers[field].model().item(2).setEnabled(True)
                    self.switchers[field].setCurrentIndex(2)

    def copyright_activated(self, index):
        """Slot function called in response to a change in copyright selector menu.

        Replaces copyright text widget contents with the corresponding text from the config file.
        """
        self.set_gui_text("ICOP", self.config["copyright"][self.config["copyright"]["list"][index]],
                          block=False)

    def update_coding_history(self, block=False):
        """Slot function called in response to a change in one of the Coding History selector menus.

        Replaces BWF Coding History text widget contents with a new Coding History text constructed from the
        current menu selections.

        Args:
            block (bool): If True, block all signals to prevent infinte recursion.
        """
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
        self.set_gui_text("CodingHistory", "".join(history_list), block)

    def save_metadata(self):
        """Slot function called in response to the "Save metadata" menu bar action.

        Performs bwfmetaedit calls to insert updated metadata into the BWF file.
        """
        def _call_bwf(file, given_key, text):
            """Convenience function to deal with annoying inconsistencies in bwfmetaedit field naming"""

            if given_key == "TimeReference":
                renamed_key = "Timereference"
            elif given_key == "CodingHistory":
                renamed_key = "History"
            else:
                renamed_key = given_key

            command = bwfio.bwfmetaedit.copy()
            command.extend(['--' + renamed_key + "=" + text, file])
            subprocess.run(command)

        current_md, changed_bwf_riff, changed_xmp = self.get_current_and_changed()

        if not changed_xmp and not changed_bwf_riff:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Metadata is unchanged. Nothing to update.")
            msg.exec_()
            return

        self.stackedWidget.setCurrentIndex(1)
        self.statusLabel.setText("Starting")
        self.progressBar.setMaximum(6)
        QtWidgets.QApplication.processEvents()

        if self.md5Check.isChecked() and self.md5Check.isEnabled():
            self.progressBar.setValue(1)
            self.statusLabel.setText("Generating MD5 digest")
            QtWidgets.QApplication.processEvents()
            command = bwfio.bwfmetaedit.copy()
            command.extend(["--MD5-embed", self.filename])
            subprocess.run(command)

        if self.original_md["TimeReference"] != '0':
            self.progressBar.setValue(2)
            self.statusLabel.setText("Saving time reference")
            QtWidgets.QApplication.processEvents()
            _call_bwf(self.filename, "TimeReference", "0")

        # Need to save coding history for last. If we don't, then for some bizarre reason there's duplication
        # of the last two characters of the history string...
        coding_history = changed_bwf_riff.pop("CodingHistory", None)

        for key in changed_bwf_riff:
            self.progressBar.setValue(3)
            self.statusLabel.setText("Saving {}".format(key))
            QtWidgets.QApplication.processEvents()
            _call_bwf(self.filename, key, current_md[key])

        if coding_history:
            self.progressBar.setValue(4)
            self.statusLabel.setText("Saving coding history")
            QtWidgets.QApplication.processEvents()
            _call_bwf(self.filename, "CodingHistory", coding_history)

        # something has changed, therefore at minimum we need to update xmp:MetadataDate
        self.progressBar.setValue(5)
        self.statusLabel.setText("Saving XMP")
        QtWidgets.QApplication.processEvents()
        bwfio.set_xmp({k: current_md[k] for k in self.xmp_fields}, self.filename)

        time.sleep(0.6)  # wait at least a little to make it less visually disconserting
        self.stackedWidget.setCurrentIndex(0)
        QtWidgets.QApplication.processEvents()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Metadata save completed")
        message_quit_button = QtWidgets.QPushButton("Quit")
        message_ok_button = QtWidgets.QPushButton("Ok")
        msg.addButton(message_quit_button, QtWidgets.QMessageBox.YesRole)
        msg.addButton(message_ok_button, QtWidgets.QMessageBox.NoRole)
        msg.setDefaultButton(message_quit_button)
        msg.exec_()
        if msg.clickedButton() == message_quit_button:
            QtCore.QCoreApplication.quit()
        else:
            # reset the GUI
            self.original_md = {}
            self.template_md = None
            self.edited_md = {}
            for field in self.gui_text_widgets.keys():
                self.set_gui_text(field, "")
            for switcher in self.switchers:
                self.switchers[switcher].setEnabled(False)
                for i in range(3):
                    self.switchers[switcher].model().item(i).setEnabled(False)

            # reload the newly-saved file
            self.original_md = self.load_file(self.filename)
            if self.original_md is not None:
                self.actionOpen.setEnabled(False)
                self.actionOpen_template.setEnabled(True)
                self.populate_file_info(self.filename, reload=True)

    def export_metadata(self):
        """Slot function called in response to the "Export metadata" menu bar action.

        Exports metadata in the current target BWF file into a PBCore XML file and optionally creates an MP3
        access file.
        """

        from autoBWF.bwf2pbcore import write_pbcore
        import autoBWF.autolame as autolame

        md, changed_bwf_riff, changed_xmp = self.get_current_and_changed()

        if changed_xmp or changed_bwf_riff:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(("You have unsaved edits. Export will result in inconsistencies between "
                         "internal and external metadata. Please save before exporting"))
            msg.exec_()
            return

        dialog = Export(self.filepath)
        accepted = dialog.exec_()
        if accepted:
            vals = dialog.get_values()
            if vals["include_ohms"]:
                ohms_file = vals["ohmsfile"]
            else:
                ohms_file = None

            md.update(bwfio.parse_bwf_description(md["Description"]))
            md["Duration"] = self.original_md["Duration"]

            if vals["outfile"]:
                write_pbcore(vals["outfile"], md, self.filename, ohms_file)

            if vals["do_lame"] and vals["mp3file"] != "":
                subprocess.call(autolame.construct_command(self.filename, vals["mp3file"], md, str(vals["vbr"])))

    def close_window(self):
        """Slot function called in response to the "Quit" menu bar action."""

        if self.filename is None:
            QtCore.QCoreApplication.quit()
            return

        current_md, changed_bwf_riff, changed_xmp = self.get_current_and_changed()

        if changed_xmp or changed_bwf_riff:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("You have unsaved edits. Are you sure you want to quit?")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                QtCore.QCoreApplication.quit()
            else:
                return
        else:
            QtCore.QCoreApplication.quit()


class Export(QtWidgets.QDialog, Ui_Export):
    """The "Export metadata" dialog box."""
    def __init__(self, path):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.outfileButton.clicked.connect(self.get_outfile)
        self.ohmsfileButton.clicked.connect(self.get_ohmsfile)
        self.mp3fileButton.clicked.connect(self.get_mp3file)

        pbcore_path = path.replace(".wav", "_pbcore.xml")
        self.outFile.insert(pbcore_path)
        mp3_path = path.replace(".wav", ".mp3")
        self.mp3File.insert(mp3_path)

    def get_outfile(self):
        filename = QFileDialog.getOpenFileName(self, "Select PBCore output file", "~")[0]
        if filename:
            self.outFile.clear()
            self.outFile.insert(str(filename))

    def get_ohmsfile(self):
        filename = QFileDialog.getOpenFileName(self, "Select OHMS file", "~")[0]
        if filename:
            self.ohmsFile.clear()
            self.ohmsFile.insert(str(filename))
            self.ohmsCheck.setChecked(True)

    def get_mp3file(self):
        filename = QFileDialog.getOpenFileName(self, "Select MP3 output file", "~")[0]
        if filename:
            self.ohmsFile.clear()
            self.mp3File.insert(str(filename))
            self.lameCheck.setChecked(True)

    def get_values(self):
        vals = {"outfile": self.outFile.text(),
                "ohmsfile": self.ohmsFile.text(),
                "mp3file": self.mp3File.text(),
                "include_ohms": self.ohmsCheck.isChecked(),
                "do_lame": self.lameCheck.isChecked(),
                "vbr": int(self.vbrLevel.text())
                }
        return vals


def main():
    import json
    import argparse

    from appdirs import AppDirs

    try:
        subprocess.check_output("bwfmetaedit")
    except FileNotFoundError:
        exit((
            "You must have the BWFMetaEdit CLI installed on your system to run autoBWF.\n"
            "Please download and install the latest version from https://mediaarea.net/BWFMetaEdit/Download.\n"
            "Note that you must install the 'CLI' version in addition to the GUI."))

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
    parser.add_argument('--config', action="store_true", help="show location of configuration file")
    args = parser.parse_args()
    filename = args.filename
    template = args.t

    if args.config:
        print('Your configuration file is ' + str(config_file.resolve()))
        exit()

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow(filename, config, template)
    form.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
