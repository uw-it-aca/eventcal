from django.core.management.base import BaseCommand, CommandError
import restclients.trumba.calendar as Calendar


class Command(BaseCommand):
    """
    List total number of the calendars by campus
    """
    help = 'List total number of the calendars by campus' +\
        '--verbose also print calendars'

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
                            action='store_true',
                            dest='verbose',
                            default=False)

    def handle(self, *args, **options):
        Command.opt = options['verbose']

        self.display_campus_cals('Bothell', Calendar.get_bot_calendars())
        self.display_campus_cals('Seattle', Calendar.get_sea_calendars())
        self.display_campus_cals('Tacoma', Calendar.get_tac_calendars())

    def display_campus_cals(self, campus, cal_dict):
        print "Total %s calendars: %d" % (campus, len(cal_dict))
        if Command.opt and cal_dict is not None:
            count = 0
            for e in cal_dict.values():
                count = count + 1
                print "%d %s" % (count, str(e))
