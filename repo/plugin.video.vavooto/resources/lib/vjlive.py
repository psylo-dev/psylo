# -*- coding: utf-8 -*-
import sys, re, requests, time, xbmcgui, xbmc, json, os, os
from resources.lib import utils
try: 
	from infotagger.listitem import ListItemInfoTag
	tagger = True
except: tagger = False

def resolve_link(link):
	_headers={"user-agent": "MediaHubMX/2", "accept": "application/json", "content-type": "application/json; charset=utf-8", "content-length": "115", "accept-encoding": "gzip", "mediahubmx-signature":utils.getAuthSignature()}
	_data={"language":"de","region":"AT","url":link,"clientVersion":"3.0.2"}
	url = "https://vavoo.to/vto-cluster/mediahubmx-resolve.json"
	return requests.post(url, data=json.dumps(_data), headers=_headers).json()[0]["url"]

def filterout(name):
	name = re.sub(r"\.\D", "", name)
	name = re.sub("( (SD|HD|FHD|UHD|H265))?( \\(BACKUP\\))? \\(\\d+\\)$", "", name)
	name = re.sub(r"(DE : | \|\w| FHD| HD\+| HD| 1080| AUSTRIA| GERMANY| DEUTSCHLAND|HEVC|RAW| SD| YOU)", "", name).strip(".")
	name = re.sub(r"\(.*\)", "", name)
	name = re.sub(r"\[.*\]", "", name)
	name = name.replace("EINS", "1").replace("ZWEI", "2").replace("DREI", "3").replace("SIEBEN", "7").replace("  ", " ").replace("TNT", "WARNER").replace("III", "3").replace("II", "2").replace("BR TV", "BR").strip()
	if "ALLGAU" in name: name = "ALLGAU TV"
	if all(ele in name for ele in ["1", "2", "3"]): name = "1-2-3 TV"
	if "HR" in name and "FERNSEHEN" in name: name = "HR"
	elif "DAS ERSTE" in name: name = "ARD - DAS ERSTE"
	elif "EURONEWS" in name: name = "EURONEWS"
	elif "NICKEL" in name: name = "NICKELODEON"
	elif "ORF" in name:
		if "SPORT" in name: name = "ORF SPORT"
		elif "3" in name: name = "ORF 3"
		elif "2" in name: name = "ORF 2"
		elif "1" in name: name = "ORF 1"
		elif "I" in name: name = "ORF 1"
	elif "SONY" in name: name = "SONY AXN" if "AXN" in name else "SONY CHANNEL"
	elif "ANIXE" in name: name = name if "+" in name else "ANIXE SERIE"
	elif "HEIMA" in name: name = "HEIMATKANAL"
	elif "SIXX" in name: name = "SIXX"
	elif "SWR" in name: name = "SWR"
	elif "CENTRAL" in name or "VIVA" in name: name = "VIVA"
	elif "BR" in name and "FERNSEHEN" in name: name = "BR"
	elif "DMAX" in name: name = "DMAX"
	elif "DISNEY" in name: name = "DISNEY CHANNEL"
	elif "KINOWELT" in name: name = "KINOWELT"
	elif "MDR" in name: name = "MDR"
	elif "NDR" in name: name = "NDR"
	elif "RBB" in name: name = "RBB"
	elif "SERVUS" in name: name = "SERVUS TV"
	elif "RTL" in name:
		if "CRIME" in name: name = "RTL CRIME"
		if "SUPER" in name: name = "SUPER RTL"
		elif "UP" in name: name = "RTL UP"
		elif "PLUS" in name: name = "RTL UP"
		elif "PASSION" in name: name = "RTL PASSION"
		elif "LIVING" in name: name = "RTL LIVING"
	elif "NITRO" in name: name = "RTL NITRO"
	elif "UNIVERSAL" in name: name = "UNIVERSAL TV"
	elif "WDR" in name: name = "WDR"
	elif "PLANET" in name: name = "PLANET"
	elif "SYFY" in name: name = "SYFY"
	elif "E!" in name: name = "E! ENTERTAINMENT"
	elif "ENTERTAINMENT" in name: name = "E! ENTERTAINMENT"
	elif "STREET" in name: name = "13TH STREET"
	elif "WUNDER" in name: name = "WELT DER WUNDER"
	elif "KAB" in name and "1" in name:
		if "CLA" in name: name = "KABEL 1 CLASSICS"
		elif "DOKU" in name: name = "KABEL 1 DOKU"
		else: name = "KABEL 1"
	elif "PRO" in name:
		if "FUN" in name: name = "PRO 7 FUN"
		elif "MAXX" in name: name = "PRO 7 MAXX"
		else: name = "PRO 7"
	elif "SKY" in name:
		if not "PREMIEREN" in name and "PREMIERE" in name:
			name = name.replace("PREMIERE", "PREMIEREN")
		if "PREMIEREN" in name and not "CINEMA" in name: name = name.replace("SKY", "SKY CINEMA")
		if "24" in name: name = "SKY CINEMA PREMIEREN +24" if "PREMIERE" in name else "SKY CINEMA +24"
		elif "ATLANTIC" in name: name = "SKY ATLANTIC"
		elif "ACTION" in name: name = "SKY CINEMA ACTION"
		elif "BEST" in name or "HITS" in name: name = "SKY CINEMA BEST OF"
		elif "CINEMA" in name and "COMEDY" in name: name = "SKY CINEMA FUN"
		elif "COMEDY" in name: name = "SKY COMEDY"
		elif "FAMI" in name: name = "SKY CINEMA FAMILY"
		elif "SHOW" in name: name = "SKY SERIEN & SHOWS"
		elif "SPECI" in name: name = "SKY CINEMA SPECIAL"
		elif "THRILLER" in name: name = "SKY CINEMA THRILLER"
		elif "FUN" in name: name = "SKY CINEMA FUN"
		elif "CLASSIC" in name: name = "SKY CINEMA CLASSICS"
		elif "NOSTALGIE" in name: name = "SKY CINEMA CLASSICS"
		elif "KRIM" in name: name = "SKY KRIMI"
		elif "SKY 24" in name: name = "SKY CINEMA 24"
		elif "CRIME" in name: name = "SKY CRIME"
	elif "NATURE" in name: name = "SKY NATURE"
	elif "ZEE" in name: name = "ZEE ONE"
	elif "DELUX" in name: name = "DELUXE MUSIC"
	elif "DISCO" in name: name = "DISCOVERY"
	elif "TLC" in name: name = "TLC"
	elif "N-TV" in name: name = "NTV"
	elif "TELE 5 TV" in name: name = "TELE 5"
	elif "N24 DOCU" in name: name = "N24 DOKU"
	elif "TAGESSCHAU24" in name: name = "TAGESSCHAU 24"
	elif "SPIEGEL TV WISSEN" in name: name = "SPIEGEL WISSEN"
	elif "HISTORY" in name: name = "HISTORY"
	elif "VISION" in name: name = "MOTORVISION"
	elif "INVESTIGATION" in name or "A&E" in name: name = "CRIME + INVESTIGATION"
	elif "AUTO" in name: name = "AUTO MOTOR SPORT"
	elif "WELT" in name: name = "WELT DER WUNDER" if "WUNDER" in name else "WELT"
	elif "NAT" in name and "GEO" in name: name = "NAT GEO WILD" if "WILD" in name else "NATIONAL GEOGRAPHIC"
	elif "3" in name and "SAT" in name: name = "3 SAT"
	elif "WARNER" in name:
		if "SERIE" in name: name = "WARNER TV SERIE"
		elif "FILM" in name: name = "WARNER TV FILM"
		elif "COMEDY" in name: name = "WARNER TV COMEDY"
	elif "VOX" in name:
		if "+" in name: name = "VOX UP"
		elif "UP" in name: name = "VOX UP"
		else: name = "VOX"
	elif "SAT" in name and "1" in name:
		if "GOLD" in name: name = "SAT 1 GOLD"
		elif "EMOT" in name: name = "SAT 1 EMOTIONS"
		else: name = "SAT 1"
	elif "REPLAY" in name or "FOX" in name: name = "FIX & FOXI" if "FIX" in name else "SKY REPLAY"
	return name

def getchannels():
	global channels
	channels = {}
	try: groups = json.loads(utils.addon.getSetting("groups"))
	except: groups = choose()

	def _getchannels(group, cursor=0, germany=False):
		global channels
		_headers={"accept-encoding": "gzip", "user-agent":"MediaHubMX/2", "accept": "application/json", "content-type": "application/json; charset=utf-8", "mediahubmx-signature": utils.getAuthSignature()}
		_data={"language":"de","region":"AT","catalogId":"vto-iptv","id":"vto-iptv","adult":False,"search":"","sort":"name","filter":{"group":group},"cursor":cursor,"clientVersion":"3.0.2"}
		r = requests.post("https://vavoo.to/vto-cluster/mediahubmx-catalog.json", data=json.dumps(_data), headers=_headers).json()
		nextCursor = r.get("nextCursor")
		items = r.get("items")
		for item in items:
			if germany:
				if any(ele in item["name"] for ele in ["DE :", " |D"]):
					name = filterout(item["name"])
					if name not in channels: channels[name] = []
					channels[name].append(item["url"])
			else:
				name = filterout(item["name"])
				if name not in channels: channels[name] = []
				channels[name].append(item["url"])
		if nextCursor: _getchannels(group, nextCursor, germany)
			
	if "Germany" in groups:
		_getchannels("Balkans", germany=True)
		
	for group in groups:
		_getchannels(group)
	
	return channels
	
def choose():
	groups=[]
	for c in requests.get("https://www2.vavoo.to/live2/index", params={"output": "json"}).json():
		if c["group"] not in groups: groups.append(c["group"])
	groups.sort()
	indicies = utils.selectDialog(groups, "Choose Groups", True)
	group = []
	if indicies:
		for i in indicies: group.append(groups[i])
		utils.addon.setSetting("groups", json.dumps(group))
		return group

def handle_wait(kanal):
	progress = xbmcgui.DialogProgress()
	create = progress.create("Abbrechen zur manuellen Auswahl", "STARTE  : %s" % kanal)
	time_to_wait = int(utils.addon.getSetting("count")) +1
	for secs in range(1, time_to_wait):
		secs_left = time_to_wait - secs
		if utils.PY2:progress.update(int(secs/time_to_wait*100),"STARTE  : %s" % kanal,"Starte Stream in  : %s" % secs_left)
		else:progress.update(int(secs/time_to_wait*100),"STARTE  : %s\nStarte Stream in  : %s" % (kanal, secs_left))
		xbmc.Monitor().waitForAbort(1)
		if (progress.iscanceled()):
			progress.close()
			return False
	progress.close()
	return True

def livePlay(name):
	m, i, title = getchannels()[name], 0, None
	if len(m) > 1:
		if utils.addon.getSetting("auto") == "0":
			# Autoplay - rotieren bei der Stream Auswahl
			# ist wichtig wenn z.B. der erste gelistete Stream nicht funzt
			if utils.addon.getSetting("idn") == name:
				i = int(utils.addon.getSetting("num")) + 1
				if i == len(m): i = 0
			utils.addon.setSetting("idn", name)
			utils.addon.setSetting("num", str(i))
			title = "%s (%s/%s)" % (name, i + 1, len(m))  # wird verwendet für infoLabels
		elif utils.addon.getSetting("auto") == "1":
			if not handle_wait(name):	# Dialog aufrufen
				cap = []
				for i, n in enumerate(m, 1):
					cap.append("STREAM %s" %i)
				i = utils.selectDialog(cap)
				if i < 0: return
			title = "%s (%s/%s)" %(name, i+1, len(m))  # wird verwendet für infoLabels
		else:
			cap=[]
			for i, n in enumerate(m, 1): cap.append("STREAM %s" %i)
			i = utils.selectDialog(cap)
			if i < 0: return
			title = "%s (%s/%s)" % (name, i + 1, len(m))  # wird verwendet für infoLabels
	n = m[i]
	o = xbmcgui.ListItem(name)
	url = resolve_link(n) # if utils.addon.getSetting("hls") == "true" else "%s?n=1&b=5&vavoo_auth=%s|User-Agent=VAVOO/2.6" % (n, getAuthSignature())
	o.setPath(url)
	if utils.addon.getSetting("hls") == "true":
		o.setMimeType("application/vnd.apple.mpegurl")
		o.setProperty("inputstreamaddon" if utils.PY2 else "inputstream" , "inputstream.adaptive")
		o.setProperty("inputstream.adaptive.manifest_type", "hls")
	elif utils.addon.getSetting("ffmpeg") == "true" and xbmc.getCondVisibility("System.HasAddon(inputstream.ffmpegdirect)"):
		o.setMimeType("application/vnd.apple.mpegurl")
		o.setProperty("inputstream", "inputstream.ffmpegdirect")
		o.setProperty("inputstream.ffmpegdirect.is_realtime_stream", "true")
		o.setProperty("inputstream.ffmpegdirect.stream_mode", "timeshift")
		if utils.addon.getSetting("openmode") != "0":
			o.setProperty("inputstream.ffmpegdirect.open_mode", "ffmpeg" if  utils.addon.getSetting("openmode") == "1" else "curl")
		o.setProperty("inputstream.ffmpegdirect.manifest_type", "hls")
	o.setProperty("IsPlayable", "true")
	title = title if title else name
	infoLabels={"title": title, "plot": "[B]%s[/B] - Stream %s von %s" % (name, i+1, len(m))}
	if tagger:
		info_tag = ListItemInfoTag(o, 'video')
		info_tag.set_info(infoLabels)
	else: o.setInfo("Video", infoLabels) # so kann man die Stream Auswahl auch sehen (Info)
	utils.set_resolved(o)
	utils.end()
			
			
def makem3u():
	m3u = ["#EXTM3U\n"]
	for name in getchannels():
		m3u.append('#EXTINF:-1 group-title="Standart",%s\nplugin://plugin.video.vavooto/?name=%s\n' % (name.strip(), name.replace("&", "%26").replace("+", "%2b").strip()))
	m3uPath = os.path.join(utils.addonprofile, "vavoo.m3u")
	with open(m3uPath ,"w") as a:
		a.writelines(m3u)
	dialog = xbmcgui.Dialog()
	ok = dialog.ok('VAVOO.TO', 'm3u erstellt in %s' % m3uPath)
		
		
def channels():
	try: lines = json.loads(utils.addon.getSetting("favs"))
	except: lines=[]
	results = getchannels()
	for name in results:
		name = name.strip()
		index = len(results[name])
		title = name if utils.addon.getSetting("stream_count") == "false" or index == 1 else "%s  (%s)" % (name, index)
		o = xbmcgui.ListItem(name)
		cm = []
		if not name in lines:
			cm.append(("zu TV Favoriten hinzufügen", "RunPlugin(%s?action=addTvFavorit&name=%s)" % (sys.argv[0], name.replace("&", "%26").replace("+", "%2b"))))
			plot = ""
		else:
			plot = "[COLOR gold]TV Favorit[/COLOR]" #% name
			cm.append(("von TV Favoriten entfernen", "RunPlugin(%s?action=delTvFavorit&name=%s)" % (sys.argv[0], name.replace("&", "%26").replace("+", "%2b"))))
		cm.append(("Einstellungen", "RunPlugin(%s?action=settings)" % sys.argv[0]))
		cm.append(("m3u erstellen", "RunPlugin(%s?action=makem3u)" % sys.argv[0]))
		o.addContextMenuItems(cm)
		infoLabels={"title": title, "plot": plot}
		if tagger:
			info_tag = ListItemInfoTag(o, 'video')
			info_tag.set_info(infoLabels)
		else: o.setInfo("Video", infoLabels)
		o.setProperty("IsPlayable", "true")
		utils.add({"name":name}, o)
	utils.sort_method()
	utils.end()

def favchannels():
	try: lines = json.loads(utils.addon.getSetting("favs"))
	except: return
	for name in getchannels():
		if not name in lines: continue
		o = xbmcgui.ListItem(name)
		cm = []
		cm.append(("von TV Favoriten entfernen", "RunPlugin(%s?action=delTvFavorit&name=%s)" % (sys.argv[0], name.replace("&", "%26").replace("+", "%2b"))))
		cm.append(("Einstellungen", "RunPlugin(%s?action=settings)" % sys.argv[0]))
		o.addContextMenuItems(cm)
		infoLabels={"title": name, "plot": "[COLOR gold]Liste der eigene Live Favoriten[/COLOR]"}
		if tagger:
			info_tag = ListItemInfoTag(o, 'video')
			info_tag.set_info(infoLabels)
		else: o.setInfo("Video", infoLabels)
		o.setProperty("IsPlayable", "true")
		utils.add({"name":name}, o)
	utils.sort_method()
	utils.end()

def change_favorit(name, delete=False):
	try: lines = json.loads(utils.addon.getSetting("favs"))
	except: lines= []
	if delete: lines.remove(name)
	else: lines.append(name)
	utils.addon.setSetting("favs", json.dumps(lines))
	if len(lines) == 0: xbmc.executebuiltin("Action(ParentDir)")
	else: xbmc.executebuiltin("Container.Refresh")