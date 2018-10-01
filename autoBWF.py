import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from tabbed import Ui_autoBWF
import subprocess
from BWFfileIO import call_bwf, get_bwf_core, get_bwf_tech


class MainWindow(QtWidgets.QMainWindow, Ui_autoBWF):
    def __init__(self, filename, config, template, parent=None):
        self.autobwf_ns = "http://ns.ukrhec.org/autoBWF/0.1"

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

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
                                  "description": self.descriptionText,
                                  "owner": self.rightsOwnerSelect,
                                  "language": self.languageLine,
                                  "interviewer": self.interviewerLine,
                                  "interviewee": self.intervieweeLine
                                 }

        self.filename = filename
        self.original_md = {}
        self.template_md = {}
        self.current_md = {}

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
            md = get_bwf_tech(config["accept-nopadding"], fname)
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
            md = get_bwf_tech(config["accept-nopadding"], fname)
            if md["Errors"] != "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(fname + " does not appear to be a valid Wave file")
                msg.exec_()
            else:
                self.actionOpen_template.setEnabled(False)
                self.populate_template_info(fname)

    def insert_default_line(self, widget, text):
        widget.clear()
        widget.insert(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.textChanged.connect(lambda: self.activate_changed(widget))

    def insert_default_box(self, widget, text):
        widget.setCurrentText(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.currentTextChanged.connect(lambda: self.activate_changed(widget))

    def insert_default_text(self, widget, text):
        widget.clear()
        widget.insertPlainText(text)
        widget.setStyleSheet("color: grey; font: italic")
        widget.textChanged.connect(lambda: self.activate_changed(widget))

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

        m = re.compile(config["filenameRegex"]).match(file)
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
                              config["repocode"] + " " +
                              date_from_filename.replace("-", "") + " " +
                              time.replace(":", ""))

            try:
                file_use = config["fileuse"][file_use]
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
                              config["repocode"] + " " +
                              date_created.replace("-", "") + " " +
                              time.replace(":", ""))

        self.update_coding_history()

        #
        # prefill defaults and insert existing values
        #

        self.original_md.update(get_bwf_core(config["accept-nopadding"], file))

        fields_to_fill = ["Description", "Originator", "OriginationDate",
                          "OriginationTime", "OriginatorReference", "CodingHistory",
                          "INAM", "ICMT", "ICRD", "ITCH", "ISFT", "ISRC", "ICOP"]
        for field in fields_to_fill:
            self.set_existing(field)

        if self.original_md["MD5Stored"] != "":
            self.md5Check.setEnabled(False)

        self.originalXmp = self.get_xmp(file)
        if self.originalXmp["description"] != "":
            self.insert_default_text(self.descriptionText, self.originalXmp["description"])
        if self.originalXmp["owner"] != "":
            self.insert_default_box(self.rightsOwnerSelect, self.originalXmp["owner"])
        if self.originalXmp["language"] != "":
            self.insert_default_line(self.languageLine, self.originalXmp["language"])
        if self.originalXmp["interviewer"] != "":
            self.insert_default_line(self.interviewerLine, self.originalXmp["interviewer"])
        if self.originalXmp["interviewee"] != "":
            self.insert_default_line(self.intervieweeLine, self.originalXmp["interviewee"])

    def set_value_from_template(self, name):
        if self.template_md[name] != "":
            self.set_gui_text(name, self.template_md[name])

    def populate_template_info(self, file):
        # replace with template values if they exist

        if file is not None:
            self.template_md.update(get_bwf_core(config["accept-nopadding"], file))

            fields_to_fill = ["CodingHistory", "INAM", "ICRD", "ITCH", "ISRC", "ICOP"]
            for field in fields_to_fill:
                self.set_value_from_template(field)

            template_xmp = self.get_xmp(file)
            if template_xmp["description"] != "":
                self.descriptionText.clear()
                self.descriptionText.insertPlainText(template_xmp["description"])
            if template_xmp["owner"] != "":
                self.rightsOwnerSelect.lineEdit().setText(template_xmp["owner"])
            if template_xmp["language"] != "":
                self.languageLine.clear()
                self.languageLine.insert(template_xmp["language"])
            if template_xmp["interviewer"] != "":
                self.interviewerLine.clear()
                self.interviewerLine.insert(template_xmp["interviewer"])
            if template_xmp["interviewee"] != "":
                self.intervieweeLine.clear()
                self.intervieweeLine.insert(template_xmp["interviewee"])

    def copyright_activated(self, index):
        self.set_gui_text("ICOP", config["copyright"][config["copyright"]["list"][index]])

    def update_coding_history(self):
        deck = self.deckSelect.currentText()
        adc = self.adcSelect.currentText()
        software = self.softwareSelect.currentText()
        media = self.mediaSelect.currentText()
        speed = self.speedSelect.currentText()
        eq = self.eqSelect.currentText()
        type = self.typeSelect.currentText()

        analogprops = [x for x in [config["deck"][deck], media, speed, eq, type] if x != ""]
        channels = {"1": "mono", "2": "stereo"}

        history_list = [
            "A=ANALOGUE,M=stereo,T=", "; ".join(analogprops),
            "\r\nA=PCM,F=", self.original_md["SampleRate"],
            ",W=", self.original_md["BitPerSample"],
            ",M=stereo,T=", config["adc"][adc],
            "\r\nA=PCM,F=", self.original_md["SampleRate"],
            ",W=" + self.original_md["BitPerSample"],
            ",M=" + channels[self.original_md["Channels"]],
            ",T=" + config["software"][software]
        ]
        self.set_gui_text("CodingHistory", "".join(history_list))

    def get_xmp(self, file):
        import libxmp

        xmpfile = libxmp.XMPFiles(file_path=file, open_forupdate=False)
        xmp = xmpfile.get_xmp()
        xmp_dict = {"owner": "", "description": "", "language": "",
                    "interviewer": "", "interviewee": ""}

        if xmp:
            try:
                xmp_dict["owner"] = xmp.get_localized_text(
                    libxmp.consts.XMP_NS_XMP_Rights, 'Owner', 'en', 'en-US')
            except libxmp.XMPError:
                pass

            try:
                xmp_dict["description"] = xmp.get_localized_text(
                    libxmp.consts.XMP_NS_DC, 'description', 'en', 'en-US')
            except libxmp.XMPError:
                pass

            languages = []
            i = 1
            while True:
                try:
                    languages.append(xmp.get_array_item(
                        libxmp.consts.XMP_NS_DC, 'language', i))
                except libxmp.XMPError:
                    xmp_dict["language"] = ";".join(languages)
                    break

                i += 1

            xmp.register_namespace(self.autobwf_ns, 'autoBWF')

            try:
                xmp_dict["interviewer"] = xmp.get_localized_text(
                    self.autobwf_ns, 'Interviewer', 'en', 'en-US')
            except libxmp.XMPError:
                pass

            try:
                xmp_dict["interviewee"] = xmp.get_localized_text(
                    self.autobwf_ns, 'Interviewee', 'en', 'en-US')
            except libxmp.XMPError:
                pass

        return xmp_dict

    def save_metadata(self):
        from libxmp import XMPFiles, consts
        from datetime import datetime

        # first the BWF and RIFF
        command = "bwfmetaedit --specialchars "
        if config["accept-nopadding"]:
            command += "--accept-nopadding "

        if self.md5Check.isChecked() and self.md5Check.isEnabled():
            subprocess.call(command + "--MD5-embed " + self.filename, shell=True)

        call_bwf(command, self.filename, "Timereference", "0")
        call_bwf(command, self.filename, "Description", self.descriptionLine.text())
        call_bwf(command, self.filename, "Originator", self.originatorLine.text())
        call_bwf(command, self.filename, "OriginatorReference", self.originatorRefLine.text())
        call_bwf(command, self.filename, "OriginationDate", self.originationDateLine.text())
        call_bwf(command, self.filename, "OriginationTime", self.originationTimeLine.text())
        call_bwf(command, self.filename, "ICOP", self.copyrightText.toPlainText())
        call_bwf(command, self.filename, "INAM", self.titleLine.text())
        call_bwf(command, self.filename, "ITCH", self.technicianBox.currentText())
        call_bwf(command, self.filename, "ICMT", self.commentText.toPlainText())
        call_bwf(command, self.filename, "ICRD", self.creationDateLine.text())
        call_bwf(command, self.filename, "ISFT", self.isftSelect.currentText())
        call_bwf(command, self.filename, "ISRC", self.sourceSelect.currentText())
        call_bwf(command, self.filename, "IARL", config["iarl"])
        call_bwf(command, self.filename, "History", self.codingHistoryText.toPlainText())
        # for some bizarre reason, --History has to be last,
        # otherwise there's duplication of the last two characters of the history string...

        # XMP must be done after RIFF, as xmp library crashes if wav has no RIFF tags
        xmpfile = XMPFiles(file_path=self.filename, open_forupdate=True)
        xmp = xmpfile.get_xmp()

        if self.rightsOwnerSelect.currentText():
            xmp.set_localized_text(
                consts.XMP_NS_XMP_Rights, 'Owner',
                'en', 'en-US', self.rightsOwnerSelect.currentText())
        if self.descriptionText.toPlainText():
            xmp.set_localized_text(
                consts.XMP_NS_DC, 'description',
                'en', 'en-US', self.descriptionText.toPlainText())

        if self.languageLine.text():
            # delete languages first to prevent appending to existing array
            xmp.delete_property(consts.XMP_NS_DC, 'language')

            for lang in self.languageLine.text().split(";"):
                xmp.append_array_item(consts.XMP_NS_DC, 'language',
                                      lang.strip(),
                                      {'prop_array_is_ordered': False,
                                       'prop_value_is_array': True})

        xmp.register_namespace(self.autobwf_ns, 'autoBWF')

        if self.interviewerLine.text():
            xmp.set_localized_text(
                self.autobwf_ns, 'Interviewer',
                'en', 'en-US', self.interviewerLine.text())
        if self.intervieweeLine.text():
            xmp.set_localized_text(
                self.autobwf_ns, 'Interviewee',
                'en', 'en-US', self.intervieweeLine.text())

        xmp.set_property_datetime(consts.XMP_NS_XMP,
                                  "MetadataDate", datetime.now())

        xmpfile.put_xmp(xmp)
        xmpfile.close_file()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Metadata saved successfully")
        msg.exec_()


if __name__ == "__main__":
    import json
    import argparse
    import autobwfconfig
    from appdirs import AppDirs
    from pathlib import Path

    default_text = autobwfconfig.default_config()

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
