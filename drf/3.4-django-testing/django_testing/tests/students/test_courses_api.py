import random
import pytest

from django.urls import reverse
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from students.models import Course
from students.serializers import CourseSerializer

def test_example():
    assert True, 'Just test example'


@pytest.mark.django_db
def test_courses_retrieve(courses_factory, api_client):
    '''
    проверка получения 1го курса (retrieve-логика)
    '''

    # создаем курс через фабрику
    course = courses_factory()

    # строим урл и делаем запрос через тестовый клиент
    url = reverse('courses-detail', args=(course.id,))
    resp = api_client.get(url)
    resp_json = resp.json()

    # проверяем, что вернулся именно тот курс, который запрашивали
    assert resp.status_code == HTTP_200_OK
    assert course.name == resp_json['name']


@pytest.mark.django_db
def test_courses_list(courses_factory, api_client):
    '''
    проверка получения списка курсов (list-логика)
    '''

    courses_factory(_quantity=4)
    url = reverse('courses-list')
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 4


@pytest.mark.django_db
def test_courses_id_filter(courses_factory, api_client):
    '''
    проверка фильтрации списка курсов по id
    '''
    courses_factory(_quantity=5)
    names = Course.objects.all()
    id_set = set()
    for name in names:
        id_set.add(name.id)
    id = random.sample(id_set, 1)[0]
    data = {'id': id}
    url = reverse('courses-list')
    resp = api_client.get(url, data=data)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['id'] == id


@pytest.mark.django_db
def test_courses_name_filter(courses_factory, api_client):
    '''
    проверка фильтрации списка курсов по name
    '''

    for i in range(5):
        courses_factory(name=f'Course {i}')
    name = 'Course 3'
    data = {'name': name}
    url = reverse('courses-list')
    resp = api_client.get(url, data=data)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['name'] == name


@pytest.mark.django_db
def test_courses_create(api_client):
    '''
    тест успешного создания курса
    '''

    url = reverse('courses-list')
    name = 'Sample course'
    data = {'name': name}
    resp = api_client.post(url, data=data)
    resp_json = resp.json()
    assert resp.status_code == HTTP_201_CREATED
    assert resp_json['name'] == name

@pytest.mark.django_db
def test_courses_update(courses_factory, api_client):
    '''
    тест успешного обновления курса
    '''
    course = courses_factory(name='Sample course')
    course_id = course.id

    new_course_name = 'New sample course'
    data = {'name': new_course_name}
    url = reverse('courses-detail', args=(course_id,))
    resp = api_client.put(url, data=data)
    new_course = Course.objects.get(id=course_id)

    assert resp.status_code == HTTP_200_OK
    assert new_course.name == new_course_name


@pytest.mark.django_db
def test_courses_delete(courses_factory, api_client):
    '''
    тест успешного удаления курса
    '''
    course = courses_factory(name='Sample course')

    url = reverse('courses-detail', args=(course.id,))
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.parametrize('student_count, expected_result', [
    (25, False),
    (20, True),
    (15, True)
])
@pytest.mark.django_db
def test_max_students_per_course(student_count, expected_result):
    '''
    тесты ограниченного числа студентов
    '''
    students_list = [{'name': f'name {i}'} for i in range(student_count)]
    name = 'Sample course'
    data = {'name': name, 'students': students_list}
    serializer = CourseSerializer()
    try:
        serializer.validate(data)
        result = True
    except serializers.ValidationError:
        result = False
    assert result == expected_result
