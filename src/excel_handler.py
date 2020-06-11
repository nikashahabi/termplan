import xlrd

from src.models import SemesterCourse, Course, Professor, Department, ChartTable


def handle_uploaded_semester_file(f):
    course = xlrd.open_workbook(file_contents=f.read())
    for sheet in course.sheets():
        try:
            number_of_rows = sheet.nrows
            for row in range(1, number_of_rows):
                department = sheet.cell(row, 0).value
                course_code = sheet.cell(row, 1).value
                course_name = sheet.cell(row, 2).value
                start_time = sheet.cell(row, 3).value
                end_time = sheet.cell(row, 4).value
                day1 = sheet.cell(row, 5).value
                day2 = sheet.cell(row, 6).value
                exam = sheet.cell(row, 7).value
                ta_time = sheet.cell(row, 8).value
                ta_day = sheet.cell(row, 9).value
                professor_name = sheet.cell(row, 10).value
                group = sheet.cell(row, 11).value
                info = sheet.cell(row, 12).value
                capacity = sheet.cell(row, 13).value
                semester = sheet.cell(row, 14).value

                dep = Department.objects.filter(name=department).first()
                course = Course.objects.filter(code=course_code).first()
                professor, _ = Professor.objects.get_or_create(name=professor_name, department=dep)
                if SemesterCourse.objects.filter(course=course).exists():
                    semester_course = SemesterCourse.objects.filter(course=course).update(semester=semester,
                                                                                          start_time=start_time,
                                                                                          end_time=end_time,
                                                                                          day1=day1, day2=day2,
                                                                                          exam=exam,
                                                                                          ta_day=ta_day,
                                                                                          professor=professor,
                                                                                          group=group,
                                                                                          info=info,
                                                                                          capacity=capacity)
                    continue

                semester_course = SemesterCourse.objects.create(semester=semester, course=course,
                                                                start_time=start_time,
                                                                end_time=end_time,
                                                                day1=day1, day2=day2,
                                                                exam=exam,
                                                                ta_day=ta_day, professor=professor,
                                                                group=group, info=info,
                                                                capacity=capacity)

            success = True
        except:
            success = False
        print(success)
    return success


def handle_uploaded_chart_table_file(f):
    table = xlrd.open_workbook(file_contents=f.read())
    for sheet in table.sheets():
        try:
            number_of_rows = sheet.nrows
            for row in range(1, number_of_rows):
                name = sheet.cell(row, 0).value
                code = sheet.cell(row, 1).value
                dep = sheet.cell(row, 2).value
                req_passed_units = sheet.cell(row, 3).value
                req_not_stared_units = sheet.cell(row, 4).value
                info = sheet.cell(row, 5).value
                dep, _ = Department.objects.get_or_create(name=name)
                if ChartTable.objects.filter(code=code).exists():
                    chart_table = ChartTable.objects.filter(code=code).update(name=name,
                                                                              code=code,
                                                                              dep=dep,
                                                                              req_passed_units=req_passed_units,
                                                                              req_not_stared_units=req_not_stared_units,
                                                                              info=info)
                    continue

                chart_table = ChartTable.objects.create(name=name,
                                                        code=code,
                                                        dep=dep,
                                                        req_passed_units=req_passed_units,
                                                        req_not_stared_units=req_not_stared_units,
                                                        info=info)

            success = True
        except:
            success = False
        print(success)
    return success


def handle_uploaded_chart_courses_file(f):
    course = xlrd.open_workbook(file_contents=f.read())
    for sheet in course.sheets():
        try:
            number_of_rows = sheet.nrows
            for row in range(1, number_of_rows):
                dep = sheet.cell(row, 0).value
                name = sheet.cell(row, 1).value
                code = sheet.cell(row, 2).value
                unit = sheet.cell(row, 3).value
                table = sheet.cell(row, 4).value
                is_starred = sheet.cell(row, 5).value
                dep = Department.objects.filter(name=dep).first()
                table = ChartTable.objects.filter(code=table, dep=dep).first()
                if Course.objects.filter(code=code).exists():
                    course = Course.objects.filter(code=code).update(name=name, code=code, unit=unit, department=dep,
                                                                     table=table, is_starred=int(is_starred))
                    continue
                course = Course.objects.create(name=name, code=code, unit=unit, department=dep,
                                               table=table, is_starred=int(is_starred))
            success = True
        except:
            success = False
        print(success)

    return success
