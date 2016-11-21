import csv
import logging
from django.core.management.base import BaseCommand, CommandError
from restclients.models.trumba import TrumbaCalendar
from restclients.gws import GWS
from accountsynchr.trumba.permission_manager import PermissionManager


class Command(BaseCommand):
    """
    Process the calendars listed in the file path given in the 1st arg,
    output their editors into the file path given in the 2nd arg.

    The format of the input file:
    publisher-accout,calendar-id,calendar-name
    idrcal@washington.edu,1019930,Athletics
    """

    def add_arguments(self, parser):
        parser.add_argument('input_csv_file')

    def handle(self, *args, **options):
        in_csv_file = options['input_csv_file']

        output_file = in_csv_file + ".editors"
        outf = open(output_file, 'w')
        writer = csv.writer(outf)

        gws = GWS()

        perm_m = PermissionManager()
        with open(in_csv_file, "rb") as f_obj:
            reader = csv.reader(f_obj)
            for row in reader:
                master_acc_id = row[0]
                cal_id = row[1]
                name = row[2]
                cal = TrumbaCalendar(cal_id,
                                     TrumbaCalendar.SEA_CAMPUS_CODE,
                                     name)
                editors = perm_m.get_editor_permissions(cal)
                if len(editors) == 0:
                    continue

                # outf.write("\n" + name + ":\n")
                outf.write(name + ":")
                editor_list = []
                for perm in editors:
                    try:
                        netid = perm.uwnetid
                        if gws.is_effective_member('uw_employee', netid):
                            editor_list.append("%s@uw.edu" % netid)
                    except Exception:
                        continue
                writer.writerow(editor_list)
        outf.close()
