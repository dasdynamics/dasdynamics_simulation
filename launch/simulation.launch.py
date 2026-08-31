import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # Аргументы запуска
    # rviz2_launch_argument_declare = DeclareLaunchArgument(
    #     'rviz2_run',
    #     default_value = 'true',
    #     description = 'Start Rviz2 when starting descriptions.'
    # )


    # Параметры окружения
    description_pkg_name = 'smartbox_description'
    description_file_name = 'main.urdf.xacro'
    # rviz2_config_file_name = 'rviz2_description_config.rviz'


    # Пути к пакетам
    description_pkg_path = get_package_share_directory(description_pkg_name)


    # Пути к файлам запуска
    description_launch_file_path = os.path.join(description_pkg_path, 'launch', 'description.launch.py')


    # Пути к конфигурационным файлам
    # rviz2_config_file_path = os.path.join(
    #     description_pkg_path,
    #     'config',
    #     rviz2_config_file_name
    # )


    # Обращение к файлам запуска
    description_launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(description_launch_file_path),
        launch_arguments = {'rviz2_run': 'false'}.items()
    )


    # Запуск
    ld = LaunchDescription()

    # ld.add_action(rviz2_launch_argument_declare)

    ld.add_action(description_launch_include)
    # ld.add_action(joint_state_publisher_node)
    # ld.add_action(rviz2_launch_node)

    return ld