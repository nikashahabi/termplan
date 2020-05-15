import xlrd
from terminator.src.models import SemesterCourse


def handle_uploaded_file(request, f):
    course = xlrd.open_workbook(file_contents=f.read())
    for sheet in course.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        for row in range(1, number_of_rows):
            semester = sheet.cell(row, 0).value
            course = sheet.cell(row, 1).value
            start_time = sheet.cell(row, 2).value
            end_time = sheet.cell(row, 3).value
            day1 = sheet.cell(row, 4).value
            day2 = sheet.cell(row, 5).value
            exam = sheet.cell(row, 6).value
            ta_time = sheet.cell(row, 8).value
            ta_day = sheet.cell(row, 7).value
            professor = sheet.cell(row, 9).value
            group = sheet.cell(row, 10).value
            info = sheet.cell(row, 11).value
            capacity = sheet.cell(row, 12).value
            # TODO:write conditions if exist

            semestercourse, created = SemesterCourse.objects.get_or_create(semester=semester, course=course,
                                                                           start_time=start_time, end_time=end_time,
                                                                           exam=exam,
                                                                           day1=day1, day2=day2, ta_time=ta_time,
                                                                           ta_day=ta_day, professor=professor,
                                                                           group=group, info=info, capacity=capacity)
