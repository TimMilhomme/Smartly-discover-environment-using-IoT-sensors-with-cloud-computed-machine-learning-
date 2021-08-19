import sys
from slam import SLAM

if __name__ == "__main__":
    # Verify user input arguments and initialize input data

    algorithm = sys.argv[1].lower()
    imu_path = sys.argv[2]
    lid_path = sys.argv[3]

    slam = SLAM(algorithm, imu_path, lid_path)
    slam.get_imu_data()
    slam.get_lidar_data()

    # Processing data
    slam.set_params()
    slam.initialize_arrays()
    slam.ekf()

    # Displaying results
    print("Plotting results\n" + 50*"=")
    slam.plot_results()



