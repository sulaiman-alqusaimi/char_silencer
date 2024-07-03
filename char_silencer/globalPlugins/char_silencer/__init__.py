import globalPluginHandler
import os
import config
from scriptHandler import script
from ui import message
import addonHandler
from controlTypes import STATE_READONLY, STATE_EDITABLE
addonHandler.initTranslation()
import speech


confspec = {
	"toggled": "boolean(default=false)",
}
config.confspec["char_silencer"] = confspec


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	controls = (8, 52, 82)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.toggled = config.conf["char_silencer"]["toggled"]

	def is_editable(self, obj):
		return (obj.role in self.controls or STATE_EDITABLE in obj.states) and not STATE_READONLY in obj.states

	def event_typedCharacter(self, obj, nextHandler, ch):

		print(self.is_editable(obj))
		if not self.is_editable(obj):
			if not self.toggled:
				print("triggered")
				speech._suppressSpeakTypedCharacters(1)
				# speech.speech.cancelSpeech()
		nextHandler()

	@script(gesture="kb:nvda+9", category="char_silencer", description=_("toggles the typing sound effects"))
	def script_togle(self, gesture):
		config.conf["char_silencer"]["toggled"] = self.toggled = not config.conf["char_silencer"]["toggled"]
		message(_("speeking characters for non-editable field is disabled")) if not self.toggled else message(_("speeking characters for non-editable field is enabled"))
