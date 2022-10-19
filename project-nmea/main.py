import sys
import math
import datetime


class xxRMC:
    def __init__(self):
        self.talker = None
        self.utc_time = None
        self.status = None
        self.latitude = None
        self.lns = None
        self.longitude = None
        self.lew = None
        self.speed_knots = None
        self.track = None
        self.date = None
        self.magnetic_variation = None
        self.mew = None
        self.faa = None
        self.checksum = None


class xxVTG:
    def __init__(self):
        self.talker = None
        self.course_true = None
        self.t = None
        self.course_magnetic = None
        self.m = None
        self.speed_knots = None
        self.n = None
        self.speed_kph = None
        self.k = None
        self.faa = None
        self.checksum = None


class xxGGA:
    def __init__(self):
        self.talker = None
        self.utc_time = None
        self.latitude = None
        self.lns = None
        self.longitude = None
        self.lew = None
        self.gps_quality = None
        self.number_of_satelites = None
        self.horizontal_dilution = None
        self.antenna_altitude = None
        self.units_of_altitude = None
        self.geoidal_separation = None
        self.units_of_separation = None
        self.age_of_dgps_data = None
        self.differential_reference_station_id = None
        self.checksum = None


class xxGSA:
    def __init__(self):
        self.talker = None
        self.selection_mode = None
        self.mode = None
        self.id1 = None
        self.id2 = None
        self.id3 = None
        self.id4 = None
        self.id5 = None
        self.id6 = None
        self.id7 = None
        self.id8 = None
        self.id9 = None
        self.id10 = None
        self.id11 = None
        self.id12 = None
        self.pdop = None
        self.hdop = None
        self.vdop = None
        self.checksum = None


class xxGSV:
    def __init__(self):
        self.talker = None
        self.number_of_gsv_sentences_in_group = None
        self.sentence_number_within_group = None
        self.number_of_satelites_in_view = None
        self.satelites = None
        self.checksum = None


class xxGLL:
    def __init__(self):
        self.talker = None
        self.latitude = None
        self.lns = None
        self.longitude = None
        self.lew = None
        self.utc_time = None
        self.status = None
        self.faa = None
        self.checksum = None


class xxGBS:
    def __init__(self):
        self.talker = None
        self.utc_time = None
        self.latitude_error = None
        self.longitude_error = None
        self.altitude_error = None
        self.satelite_id = None
        self.missed_probability = None
        self.bias_meters = None
        self.sd = None  # Standard deviation
        self.checksum = None


class xxGNS:
    def __init__(self):
        self.talker = None
        self.utc_time = None
        self.latitude = None
        self.lns = None
        self.longitude = None
        self.lew = None
        self.mode = None
        self.number_of_satelites = None
        self.hdop = None
        self.antenna_altitude = None
        self.geoidal_separation = None
        self.age_of_differential_data = None
        self.differential_reference_station_id = None
        self.navigation_status = None
        self.checksum = None


class trkpt:
    def __init__(self):
        self.lat = ""
        self.lon = ""
        self.ele = ""
        self.date = ""  # 2020-11-04 # merge with time
        self.time = ""  # T00:00:41Z # merge with date
        self.fix = ""
        self.sat = ""
        self.hdop = ""
        self.vdop = ""
        self.pdop = ""
        self.geoidheight = ""
        self.magvar = ""  # 0.0 <= value < 360.0
        self.e_nmea_speed = ""
        self.e_nmea_course = ""
        self.e_nmea_satelites = ""

    def __str__(self):
        if self.lat == "" or self.lon == "":
            return ""
        body = ""
        if self.ele != "":
            body += "<ele>{0}</ele>".format(self.ele)
        if self.date != "" and self.time != "":
            body += "<time>{0}{1}</time>".format(self.date, self.time)
        if self.fix != "":
            body += "<fix>{0}</fix>".format(self.fix)
        if self.sat != "":
            body += "<sat>{0}</sat>".format(self.sat)
        if self.hdop != "":
            body += "<hdop>{0}</hdop>".format(self.hdop)
        if self.vdop != "":
            body += "<vdop>{0}</vdop>".format(self.vdop)
        if self.pdop != "":
            body += "<pdop>{0}</pdop>".format(self.pdop)
        if self.geoidheight != "":
            body += "<geoidheight>{0}</geoidheight>".format(self.geoidheight)
        if self.magvar != "":
            body += "<magvar>{0}</magvar>".format(self.magvar)
        if self.e_nmea_speed != "" or self.e_nmea_course != "" or self.e_nmea_satelites != "":
            extensions = ""
            if self.e_nmea_speed != "":
                extensions += "<project-nmea:speed>{0}</project-nmea:speed>".format(self.e_nmea_speed)
            if self.e_nmea_course != "":
                extensions += "<project-nmea:course>{0}</project-nmea:course>".format(self.e_nmea_course)
            if self.e_nmea_satelites != "":
                extensions += "<project-nmea:satelites>{0}</project-nmea:satelites>".format(self.e_nmea_satelites)
            body += "<extensions>{0}</extensions>".format(extensions)
        return "<trkpt lat=\"{0}\" lon=\"{1}\">{2}</trkpt>".format(self.lat, self.lon, body)


class satelite_extension:
    def __init__(self):
        self.e_sat_id = ""
        self.e_sat_elevation = ""
        self.e_sat_azimuth = ""
        self.e_sat_snr = ""

    def __str__(self):
        return "<project-nmea:satelite id=\"{0}\" ele=\"{1}\" azi=\"{2}\" snr=\"{3}\"></project-nmea:satelite>".format(self.e_sat_id,
                                                                                                       self.e_sat_elevation,
                                                                                                       self.e_sat_azimuth,
                                                                                                       self.e_sat_snr)


class ProgramSettings:
    def __init__(self):
        self.input_file_name = None
        self.output_file_name = None
        self.filter_talker = None
        self.filter_time = None  #
        self.filter_length = None  #
        self.filter_relation_function = (lambda x, y: x or y)  #
        self.filter_length_function = None  # (lat1, lon1, lat2, lon2)
        self.number_of_exceptions = 0
        self.number_of_processed_lines = 0


class NmeaInvalidLine(Exception):
    def __init__(self, line):
        self.line = line


class NmeaInvalidChecksum(Exception):
    def __init__(self, line):
        self.line = line


################################################################################################################################
################################################################################################################################
################################################################################################################################

def nmea_checksum(sentence=''):
    checksum_index = sentence.rfind('*')
    if checksum_index < 0:
        return False
    checksum = sentence[checksum_index + 1:checksum_index + 3]
    sentence_bytes = sentence[1:checksum_index].encode("utf-8", "ignore")
    result = 0
    for b in sentence_bytes:
        result ^= b
    return result == bytearray.fromhex(checksum)[0]


def haversine_length(lat1, lon1, lat2, lon2):
    # http://www.movable-type.co.uk/scripts/latlong.html
    R = 6371e3
    p1 = lat1 * math.pi / 180.0
    p2 = lat2 * math.pi / 180.0
    dp = (lat2 - lat1) * math.pi / 180.0
    da = (lon2 - lon1) * math.pi / 180.0
    a = math.sin(dp / 2.0) * math.sin(dp / 2) + math.cos(p1) * math.cos(p2) * math.sin(da / 2.0) * math.sin(da / 2.0)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    result = R * c
    return result


def get_seconds_difference(utc1, utc2):
    year1 = int(utc1[0:4])
    month1 = int(utc1[4:6])
    day1 = int(utc1[6:8])
    hour1 = int(utc1[9:11])
    minute1 = int(utc1[11:13])
    second1 = int(utc1[13:15])
    year2 = int(utc2[0:4])
    month2 = int(utc2[4:6])
    day2 = int(utc2[6:8])
    hour2 = int(utc2[9:11])
    minute2 = int(utc2[11:13])
    second2 = int(utc2[13:15])
    dt1 = datetime.datetime(year1, month1, day1, hour1, minute1, second1)
    dt2 = datetime.datetime(year2, month2, day2, hour2, minute2, second2)
    result = abs((dt1 - dt2).total_seconds())
    return result


def get_angsec_difference(lat1, lon1, lat2, lon2):
    p1 = lat1 * math.pi / 180.0
    p2 = lat2 * math.pi / 180.0
    da = (lon2 - lon1) * math.pi / 180.0
    result = (math.acos(math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(da)) / (
                math.pi / 180.0)) * 3600.0
    return result


# nmea_files = []
# nmea_files.append("project-nmea\\2008-08-06-08-53-42.project-nmea") # 0
# nmea_files.append("project-nmea\\2013-12-31.project-nmea") # 1
# nmea_files.append("project-nmea\\2014-10-19.project-nmea") # 2
# nmea_files.append("project-nmea\\2014-10-25.project-nmea") # 3
# nmea_files.append("project-nmea\\2015-08-12.project-nmea") # 4
# nmea_files.append("project-nmea\\2017-11-02.project-nmea") # 5
# nmea_files.append("project-nmea\\20080904-105553.project-nmea") # 6
# nmea_files.append("project-nmea\\20080904-115203.project-nmea") # 7
# nmea_files.append("project-nmea\\20080904-141417.project-nmea") # 8
# nmea_files.append("project-nmea\\20090804-174057.project-nmea") # 9
# nmea_files.append("project-nmea\\20090811-194434.project-nmea") # 10
# nmea_files.append("project-nmea\\20090811-210505.project-nmea") # 11
# nmea_files.append("project-nmea\\20090814-092132.project-nmea") # 12
# nmea_files.append("project-nmea\\COM33_180817_192414.project-nmea") # 13

# -filter:talker   [op1+op2+op3+...+opN] # 0.5 bodu
# -filter:angsec   [integer] # 0.5 bodu
# -filter:seconds  [integer] # 0.5 bodu
# -filter:meters   [integer] # 1.0 bodu
# -filter:relation [and][or] # 0.0 bodu

program = ProgramSettings()
option = ""
for index, item in enumerate(sys.argv):
    if index > 0:
        if option != "":
            if option == "-filter:talker":
                option = ""
                program.filter_talker = [s.lower() for s in item.split("+")]
                continue
            elif option == "-filter:angsec":
                option = ""
                program.filter_length = float(item)
                program.filter_length_function = get_angsec_difference
                continue
            elif option == "-filter:seconds":
                option = ""
                program.filter_time = float(item)
                continue
            elif option == "-filter:meters":
                option = ""
                program.filter_length = float(item)
                program.filter_length_function = haversine_length
                continue
            elif option == "-filter:relation":
                option = ""
                if item.lower() == "and":
                    program.filter_relation_function = (lambda x, y: x and y)
                elif item.lower() == "or":
                    program.filter_relation_function = (lambda x, y: x or y)
                else:
                    print("Invalid -filter:relation parameter")
                continue
            elif option == "-input":
                option = ""
                program.input_file_name = item
                continue
            elif option == "-output":
                option = ""
                program.output_file_name = item
                if not item.lower().endswith(".gpx"):
                    program.output_file_name += ".gpx"
                continue
            else:
                option = ""
                print("invalid parameter: {0}".format(item))
                continue
        if item.lower() == "-filter:talker" or item.lower() == "-ft":
            option = "-filter:talker"
            continue
        elif item.lower() == "-filter:angsec" or item.lower() == "-fa":
            option = "-filter:angsec"
            continue
        elif item.lower() == "-filter:seconds" or item.lower() == "-fs":
            option = "-filter:seconds"
            continue
        elif item.lower() == "-filter:meters" or item.lower() == "-fm":
            option = "-filter:meters"
            continue
        elif item.lower() == "-filter:relation" or item.lower() == "-fr":
            option = "-filter:relation"
            continue
        elif item.lower() == "-input" or item.lower() == "-i":
            option = "-input"
            continue
        elif item.lower() == "-output" or item.lower() == "-o":
            option = "-output"
            continue
        else:
            if program.input_file_name == None:
                program.input_file_name = item
            elif program.output_file_name == None:
                program.output_file_name = item
                if not item.lower().endswith(".gpx"):
                    program.output_file_name += ".gpx"
            else:
                print("invalid parameter: {0}".format(item))
            continue

# program.input_file_name = "project-nmea\\2008-08-06-08-53-42.project-nmea"
# program.filter_seconds = 30.0

if program.output_file_name == None and program.input_file_name != None:
    file_extension_index = program.input_file_name.lower().rfind(".project-nmea")
    if file_extension_index > 0:
        program.output_file_name = program.input_file_name[:file_extension_index] + ".gpx"
    else:
        program.output_file_name = program.input_file_name + ".gpx"

# print("---- START ----")
# print(program.input_file_name)
# print(program.output_file_name)
# print(program.filter_talker)
# print(program.filter_angsec)
# print(program.filter_seconds)
# print(program.filter_meters)
# print(program.filter_relation_function)
# print("----  END  ----")

if program.input_file_name == program.output_file_name:
    raise NameError("input_file_name == output_file_name")

lines = []
with open(program.input_file_name) as f:
    lines = f.readlines()

sentences = []
for line_number, line in enumerate(lines):
    try:
        line_start_index = line.find('$')
        line_checksum_index = line.rfind('*')
        if line_start_index < 0 or line_checksum_index < 0 or line_start_index > line_checksum_index:
            raise NmeaInvalidLine(line)

        line_sentence = line[line_start_index:line_checksum_index + 3]
        if not nmea_checksum(line_sentence):
            raise NmeaInvalidChecksum(line)

        checksum_index = line_sentence.rfind('*')
        line_tokens = line_sentence[7:checksum_index].split(',')
        talker = line_sentence[1:3]
        sentence_type = line_sentence[3:6]
        checksum = line_sentence[checksum_index + 1:checksum_index + 3]
        if sentence_type == "RMC":
            sentence = xxRMC()
            sentence.talker = talker
            sentence.utc_time = line_tokens[0]
            sentence.status = line_tokens[1]
            sentence.latitude = line_tokens[2]
            sentence.lns = line_tokens[3]
            sentence.longitude = line_tokens[4]
            sentence.lew = line_tokens[5]
            sentence.speed_knots = line_tokens[6]
            sentence.track = line_tokens[7]
            sentence.date = line_tokens[8]
            sentence.magnetic_variation = line_tokens[9]
            sentence.mew = line_tokens[10]
            sentence.faa = line_tokens[11] if len(line_tokens) == 12 else ''  # FAA mode indicator (NMEA 2.3 and later)
            sentence.checksum = checksum
            sentences.append(sentence)
        elif sentence_type == "VTG":
            sentence = xxVTG()
            sentence.talker = talker
            sentence.course_true = line_tokens[0]
            sentence.t = line_tokens[1]
            sentence.course_magnetic = line_tokens[2]
            sentence.m = line_tokens[3]
            sentence.speed_knots = line_tokens[4]
            sentence.n = line_tokens[5]
            sentence.speed_kph = line_tokens[6]
            sentence.k = line_tokens[7]
            sentence.faa = line_tokens[8] if len(line_tokens) == 9 else ''  # FAA mode indicator (NMEA 2.3 and later)
            sentence.checksum = checksum
            sentences.append(sentence)
        elif sentence_type == "GGA":
            sentence = xxGGA()
            sentence.talker = talker
            sentence.utc_time = line_tokens[0]
            sentence.latitude = line_tokens[1]
            sentence.lns = line_tokens[2]
            sentence.longitude = line_tokens[3]
            sentence.lew = line_tokens[4]
            sentence.gps_quality = line_tokens[5]
            sentence.number_of_satelites = line_tokens[6]
            sentence.horizontal_dilution = line_tokens[7]
            sentence.antenna_altitude = line_tokens[8]
            sentence.units_of_altitude = line_tokens[9]
            sentence.geoidal_separation = line_tokens[10]
            sentence.units_of_separation = line_tokens[11]
            sentence.age_of_dgps_data = line_tokens[12]
            sentence.differential_reference_station_id = line_tokens[13]
            sentence.checksum = checksum
            sentences.append(sentence)
        elif sentence_type == "GSA":
            sentence = xxGSA()
            sentence.talker = talker
            sentence.selection_mode = line_tokens[0]
            sentence.mode = line_tokens[1]
            sentence.id1 = line_tokens[2]
            sentence.id2 = line_tokens[3]
            sentence.id3 = line_tokens[4]
            sentence.id4 = line_tokens[5]
            sentence.id5 = line_tokens[6]
            sentence.id6 = line_tokens[7]
            sentence.id7 = line_tokens[8]
            sentence.id8 = line_tokens[9]
            sentence.id9 = line_tokens[10]
            sentence.id10 = line_tokens[11]
            sentence.id11 = line_tokens[12]
            sentence.id12 = line_tokens[13]
            sentence.pdop = line_tokens[14]
            sentence.hdop = line_tokens[15]
            sentence.vdop = line_tokens[16]
            sentence.checksum = checksum
            sentences.append(sentence)
        elif sentence_type == "GSV":
            sentence = xxGSV()
            sentence.talker = talker
            sentence.number_of_gsv_sentences_in_group = line_tokens[0]
            sentence.sentence_number_within_group = line_tokens[1]
            sentence.number_of_satelites_in_view = line_tokens[2]
            sentence.satelites = line_tokens[3:]
            sentence.checksum = checksum
            sentences.append(sentence)
        elif sentence_type == "GLL":
            sentence = xxGLL()
            sentence.talker = talker
            sentence.latitude = line_tokens[0]
            sentence.lns = line_tokens[1]
            sentence.longitude = line_tokens[2]
            sentence.lew = line_tokens[3]
            sentence.utc_time = line_tokens[4]
            sentence.status = line_tokens[5]
            sentence.faa = line_tokens[6] if len(line_tokens) == 7 else ''  # FAA mode indicator (NMEA 2.3 and later)
            sentence.checksum = checksum
            sentences.append(sentence)
        elif sentence_type == "GBS":
            sentence = xxGBS()
            sentence.talker = talker
            sentence.utc_time = line_tokens[0]
            sentence.latitude_error = line_tokens[1]
            sentence.longitude_error = line_tokens[2]
            sentence.altitude_error = line_tokens[3]
            sentence.satelite_id = line_tokens[4]
            sentence.missed_probability = line_tokens[5]
            sentence.bias_meters = line_tokens[6]
            sentence.sd = line_tokens[7]
            sentence.checksum = checksum
            sentences.append(sentence)
        elif sentence_type == "GNS":
            sentence = xxGNS()
            sentence.talker = talker
            sentence.utc_time = line_tokens[0]
            sentence.latitude = line_tokens[1]
            sentence.lns = line_tokens[2]
            sentence.longitude = line_tokens[3]
            sentence.lew = line_tokens[4]
            sentence.mode = line_tokens[5]
            sentence.number_of_satelites = line_tokens[6]
            sentence.hdop = line_tokens[7]
            sentence.antenna_altitude = line_tokens[8]
            sentence.geoidal_separation = line_tokens[9]
            sentence.age_of_differential_data = line_tokens[10]
            sentence.differential_reference_station_id = line_tokens[11]
            sentence.navigation_status = line_tokens[12] if len(line_tokens) == 13 else ''  # optional
            sentence.checksum = checksum
            sentences.append(sentence)
        elif sentence_type == "GNQ":
            pass  # Veta GNQ se vyskytuje pouze jednou, a to v souboru COM33_180817_192414.project-nmea
        else:
            print("unprocessed sentence_type {0}".format(sentence_type))
            print(line)
        program.number_of_processed_lines += 1
    except IndexError:
        print("IndexError: line {0}; file \"{1}\" content:\n{2}".format(line_number, program.input_file_name, line))
        program.number_of_exceptions += 1
    except NmeaInvalidLine:
        print(
            "NmeaInvalidLine: line {0}; file \"{1}\" content:\n{2}".format(line_number, program.input_file_name, line))
        program.number_of_exceptions += 1
    except NmeaInvalidChecksum:
        print("NmeaInvalidChecksum: line {0}; file \"{1}\" content:\n{2}".format(line_number, program.input_file_name,
                                                                                 line))
        program.number_of_exceptions += 1
    except:
        print(
            "Unexpected error: line {0}; file \"{1}\" content:\n{2}".format(line_number, program.input_file_name, line))
        program.number_of_exceptions += 1

trkpt_list = []  # list instanci trkpt
current_satelites = {}  # dict instanci satelite_extension
nmea_utc_time = ""
lat_gpx = ""
lon_gpx = ""
ele_gpx = ""
date_gpx = ""
time_gpx = ""
fix_gpx = ""
sat_gpx = ""
hdop_gpx = ""
vdop_gpx = ""
pdop_gpx = ""
geoidheight_gpx = ""
magvar_gpx = ""
e_nmea_speed_gpx = ""
e_nmea_course_gpx = ""
filter_last_lat = None
filter_last_lon = None
filter_last_utc = None
for sentence in sentences:
    if program.filter_talker != None:
        if sentence.talker.lower() not in program.filter_talker:
            continue
    if (type(sentence) in [xxRMC, xxGGA, xxGLL, xxGBS, xxGNS]):
        if nmea_utc_time == "":
            nmea_utc_time = sentence.utc_time
        if nmea_utc_time != "" and sentence.utc_time != "" and sentence.utc_time != nmea_utc_time:
            if lat_gpx != "" and lon_gpx != "":
                current_point = trkpt()
                current_point.lat = lat_gpx
                current_point.lon = lon_gpx
                current_point.ele = ele_gpx
                current_point.date = date_gpx
                current_point.time = time_gpx
                current_point.fix = fix_gpx
                current_point.sat = sat_gpx
                current_point.hdop = hdop_gpx
                current_point.vdop = vdop_gpx
                current_point.pdop = pdop_gpx
                current_point.geoidheight = geoidheight_gpx
                current_point.magvar = magvar_gpx
                current_point.e_nmea_speed = e_nmea_speed_gpx
                current_point.e_nmea_course = e_nmea_course_gpx
                current_point.e_nmea_satelites = ''.join([str(v) for k, v in current_satelites.items()])
                trkpt_list.append(current_point)
            current_satelites = {}
            lat_gpx = ""
            lon_gpx = ""
            ele_gpx = ""
            # date_gpx = ""
            time_gpx = ""
            fix_gpx = ""
            sat_gpx = ""
            hdop_gpx = ""
            vdop_gpx = ""
            pdop_gpx = ""
            geoidheight_gpx = ""
            magvar_gpx = ""
            e_nmea_speed_gpx = ""
            e_nmea_course_gpx = ""
            nmea_utc_time = sentence.utc_time
    if isinstance(sentence, xxRMC):  # pozice
        if (sentence.status.upper() != "A" or sentence.latitude == "" or sentence.longitude == ""):
            continue
        lat_split = sentence.latitude.split('.')
        lon_split = sentence.longitude.split('.')
        lat_gpx = ('-' if sentence.lns.upper() == 'S' else '') + lat_split[0][:-2] + str(
            float(lat_split[0][-2:] + '.' + lat_split[1]) / 60.0)[1:]
        lon_gpx = ('-' if sentence.lew.upper() == 'W' else '') + lon_split[0][:-2] + str(
            float(lon_split[0][-2:] + '.' + lon_split[1]) / 60.0)[1:]
        date_gpx = (sentence.date[4:] if len(sentence.date[4:]) == 4 else "20" + sentence.date[4:]) + (
                    sentence.date[2:4] + sentence.date[0:2]) if sentence.date != "" else ""
        time_gpx = 'T' + sentence.utc_time + 'Z' if sentence.utc_time != "" else ""
        e_nmea_speed_gpx = str(float(sentence.speed_knots) * 0.51444444444) if sentence.speed_knots != "" else ""
        e_nmea_course_gpx = sentence.track
        magvar_gpx = ('-' if sentence.mew.upper() == 'W' else '') + sentence.magnetic_variation
        print(end='')
    elif isinstance(sentence, xxVTG):  # pozice
        e_nmea_speed_gpx = str((float(sentence.speed_kph) / 3.6 + float(
            sentence.speed_knots) * 0.51444444444) / 2.0) if sentence.speed_kph != "" and sentence.speed_knots != "" else ""
        e_nmea_course_gpx = sentence.course_true
        magvar_gpx = str(float(sentence.course_true) - float(
            sentence.course_magnetic)) if magvar_gpx == "" and sentence.course_true != "" and sentence.course_magnetic != "" else ""
        print(end='')
    elif isinstance(sentence, xxGGA):  # pozice
        if (sentence.latitude == "" or sentence.longitude == "" or sentence.gps_quality in ["", "0"]):
            continue
        time_gpx = 'T' + sentence.utc_time + 'Z' if sentence.utc_time != "" else ""
        lat_split = sentence.latitude.split('.')
        lon_split = sentence.longitude.split('.')
        lat_gpx = ('-' if sentence.lns.upper() == 'S' else '') + lat_split[0][:-2] + str(
            float(lat_split[0][-2:] + '.' + lat_split[1]) / 60.0)[1:]
        lon_gpx = ('-' if sentence.lew.upper() == 'W' else '') + lon_split[0][:-2] + str(
            float(lon_split[0][-2:] + '.' + lon_split[1]) / 60.0)[1:]
        fix_gpx = "dgps" if sentence.gps_quality == "2" else "pps" if sentence.gps_quality == "3" else ""
        sat_gpx = sentence.number_of_satelites if sat_gpx == "" else sat_gpx
        geoidheight_gpx = sentence.geoidal_separation
        ele_gpx = sentence.antenna_altitude if sentence.antenna_altitude != "" else ele_gpx
        print(end='')
    elif isinstance(sentence, xxGSA):  # satelity
        fix_gpx = sentence.mode + 'd' if fix_gpx == "" and (sentence.mode == "2" or sentence.mode == "3") else fix_gpx
        hdop_gpx = sentence.hdop
        vdop_gpx = sentence.vdop
        pdop_gpx = sentence.pdop
        if sentence.id1 != "":
            sat_id = str(int(sentence.id1))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id2 != "":
            sat_id = str(int(sentence.id2))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id3 != "":
            sat_id = str(int(sentence.id3))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id4 != "":
            sat_id = str(int(sentence.id4))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id5 != "":
            sat_id = str(int(sentence.id5))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id6 != "":
            sat_id = str(int(sentence.id6))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id7 != "":
            sat_id = str(int(sentence.id7))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id8 != "":
            sat_id = str(int(sentence.id8))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id9 != "":
            sat_id = str(int(sentence.id9))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id10 != "":
            sat_id = str(int(sentence.id10))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id11 != "":
            sat_id = str(int(sentence.id11))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
        if sentence.id12 != "":
            sat_id = str(int(sentence.id12))
            if sat_id not in current_satelites:
                current_satelites[sat_id] = satelite_extension()
            current_satelites[sat_id].e_sat_id = sat_id
    elif isinstance(sentence, xxGSV):  # satelity
        sat_gpx = sentence.number_of_satelites_in_view
        sat_id = ""
        for i, v in enumerate(sentence.satelites):
            if i % 4 == 0:
                if v == "" or v == "0":
                    break
                sat_id = str(int(v))
                if sat_id not in current_satelites:
                    current_satelites[sat_id] = satelite_extension()
                current_satelites[sat_id].e_sat_id = sat_id
            if i % 4 == 1:
                current_satelites[sat_id].e_sat_elevation = v
            if i % 4 == 2:
                current_satelites[sat_id].e_sat_azimuth = v
            if i % 4 == 3:
                current_satelites[sat_id].e_sat_snr = v
    elif isinstance(sentence, xxGLL):  # pozice
        if (sentence.status.upper() != "A" or sentence.latitude == "" or sentence.longitude == ""):
            continue
        lat_split = sentence.latitude.split('.')
        lon_split = sentence.longitude.split('.')
        lat_gpx = ('-' if sentence.lns.upper() == 'S' else '') + lat_split[0][:-2] + str(
            float(lat_split[0][-2:] + '.' + lat_split[1]) / 60.0)[1:]
        lon_gpx = ('-' if sentence.lew.upper() == 'W' else '') + lon_split[0][:-2] + str(
            float(lon_split[0][-2:] + '.' + lon_split[1]) / 60.0)[1:]
        time_gpx = 'T' + sentence.utc_time + 'Z' if sentence.utc_time != "" else ""
    elif isinstance(sentence, xxGBS):  # satelity
        # GPS Satellite Fault Detection
        # tady k zadani neni treba nic
        pass
    elif isinstance(sentence, xxGNS):  # pozice
        if (sentence.navigation_status.upper() != "S" or sentence.latitude == "" or sentence.longitude == ""):
            continue
        time_gpx = 'T' + sentence.utc_time + 'Z' if sentence.utc_time != "" else ""
        lat_split = sentence.latitude.split('.')
        lon_split = sentence.longitude.split('.')
        lat_gpx = ('-' if sentence.lns.upper() == 'S' else '') + lat_split[0][:-2] + str(
            float(lat_split[0][-2:] + '.' + lat_split[1]) / 60.0)[1:]
        lon_gpx = ('-' if sentence.lew.upper() == 'W' else '') + lon_split[0][:-2] + str(
            float(lon_split[0][-2:] + '.' + lon_split[1]) / 60.0)[1:]
        sat_gpx = sentence.number_of_satelites
        hdop_gpx = sentence.hdop
        geoidheight_gpx = sentence.geoidal_separation
        ele_gpx = sentence.antenna_altitude if sentence.antenna_altitude != "" else ele_gpx

trkpt_list_str = []
last_datetime = None
last_lat = None
last_lon = None
for item in trkpt_list:

    if program.filter_length != None and program.filter_time != None:
        if last_datetime != None and last_lat != None and last_lon != None:
            condition_length = (
                        program.filter_length <= program.filter_length_function(float(item.lat), float(item.lon),
                                                                                last_lat, last_lon))
            condition_time = (program.filter_time <= get_seconds_difference(item.date + item.time, last_datetime))
            if program.filter_relation_function(condition_time, condition_length):
                last_datetime = item.date + item.time
                last_lat = float(item.lat)
                last_lon = float(item.lon)
                trkpt_list_str.append(str(item))
        elif item.date != "" and item.time != "":
            last_datetime = item.date + item.time
            last_lat = float(item.lat)
            last_lon = float(item.lon)
            trkpt_list_str.append(str(item))

    elif program.filter_length != None:
        if last_lat != None and last_lon != None:
            if (program.filter_length <= program.filter_length_function(float(item.lat), float(item.lon), last_lat,
                                                                        last_lon)):
                last_lat = float(item.lat)
                last_lon = float(item.lon)
                trkpt_list_str.append(str(item))
        else:
            last_lat = float(item.lat)
            last_lon = float(item.lon)
            trkpt_list_str.append(str(item))

    elif program.filter_time != None:
        if last_datetime != None:
            if (program.filter_time <= get_seconds_difference(item.date + item.time, last_datetime)):
                last_datetime = item.date + item.time
                trkpt_list_str.append(str(item))
        elif item.date != "" and item.time != "":
            last_datetime = item.date + item.time
            trkpt_list_str.append(str(item))

    else:
        trkpt_list_str.append(str(item))

trkseg_string = ''.join(trkpt_list_str)
gpx_string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><gpx version=\"1.1\" creator=\"pec0100\"><trk><trkseg>{0}</trkseg></trk></gpx>".format(
    trkseg_string)
with open(program.output_file_name, "w") as f:
    f.write(gpx_string)

print("exceptions: {0}\nprocessed: {1}".format(program.number_of_exceptions, program.number_of_processed_lines))
