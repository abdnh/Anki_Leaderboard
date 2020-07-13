from aqt import mw
from aqt.utils import showInfo

def write_config(name, value):
	config = mw.addonManager.getConfig(__name__)

	config_content = {"username": config["username"], "friends": config["friends"], "newday": config["newday"], 
	"subject": config["subject"], "country": config["country"], "scroll": config["scroll"], "refresh": config["refresh"],
	"tab": config["tab"], "token": config["token"], "achievement": config["achievement"], "sortby": config["sortby"]}

	config_content[name] = value
	mw.addonManager.writeConfig(__name__, config_content)