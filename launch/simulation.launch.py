import os
from launch import LaunchDescription
from launch_ros.actions import Node
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
    robot_name = 'SmartBox'

    simulation_pkg_name = 'dasdynamics_simulation'

    description_pkg_name = 'smartbox_description'
    description_file_name = 'main.urdf.xacro'

    gazebo_pkg_name = 'ros_gz_sim'
    gazebo_config_file_name = 'gz_bridge_config.yaml'
    gazebo_world_file_name = 'dasdynamic_test_world1.sdf'
    # gazebo_world_file_name = 'test_world.sdf'

    
    # rviz2_config_file_name = 'rviz2_description_config.rviz'


    # Пути к пакетам
    description_pkg_path = get_package_share_directory(description_pkg_name)
    gazebo_pkg_path = get_package_share_directory(gazebo_pkg_name)
    simulation_pkg_path = get_package_share_directory(simulation_pkg_name)


    # Пути к файлам
    description_launch_file_path = os.path.join(description_pkg_path, 'launch', 'description.launch.py')
    gazebo_launch_file_path = os.path.join(gazebo_pkg_path, 'launch', 'gz_sim.launch.py')
    gz_bridge_config_file_path = os.path.join(simulation_pkg_path, 'configs', gazebo_config_file_name)
    gazebo_world_file_path = os.path.join(simulation_pkg_path, 'worlds', gazebo_world_file_name)


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

    gazebo_launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file_path),
        launch_arguments = {
            'gz_args': f'-r {gazebo_world_file_path}'
        }.items()
    )


    # Ноды
    spawn_robot_in_gazebo_node = Node(
        package = 'ros_gz_sim',
        executable = 'create', 
        output = 'screen',
        arguments = [
            '-name', robot_name,
            '-topic', 'robot_description',   
        ]
    )

    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        parameters=[{
            'config_file': gz_bridge_config_file_path
            }],  
    )


    # Запуск
    ld = LaunchDescription()

    # ld.add_action(rviz2_launch_argument_declare)

    ld.add_action(description_launch_include)
    ld.add_action(gazebo_launch_include)
    ld.add_action(spawn_robot_in_gazebo_node)
    ld.add_action(gz_bridge_node)

    return ld