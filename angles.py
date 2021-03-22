import numpy as np
import matplotlib.pyplot as plt
import os


def calculate_angle(knee, hip, ankle):
    hip = [hip[0] - knee[0], hip[1] - knee[1], hip[2] - knee[2]]
    ankle = [ankle[0] - knee[0], ankle[1] - knee[1], ankle[2] - ankle[2]]
    theta = np.arccos(((hip[0]*ankle[0])+(hip[1]*ankle[1])+(hip[2]*ankle[2])) /
                      (np.sqrt(np.square(hip[0]) + np.square(hip[1]) + np.square(hip[2])) *
                       np.sqrt(np.square(ankle[0]) + np.square(ankle[1]) + np.square(ankle[2]))))
    return np.rad2deg(theta)


def main():
    path = 'Files/output/'
    files = [file for file in os.listdir(path) if file.endswith('.npy')]
    count, fig = 0, 1
    for i in range(len(files)):
        count += 1
        if count > 4:
            count = 1
            fig += 1
        anglelist = [[], [], [], [], [], []]
        data = np.load(path + files[i])
        for j in range(len(data)):
            keypoints = data[j]
            hip_l = keypoints[1]
            hip_r = keypoints[4]
            knee_l = keypoints[2]
            knee_r = keypoints[5]
            ankle_l = keypoints[3]
            ankle_r = keypoints[6]

            bottom_torso = keypoints[0]
            center_torso = keypoints[7]
            upper_torso = keypoints[8]

            center_ground = (ankle_l + ankle_r) / 2
            center_knee = (knee_l + knee_r) / 2
            center_hip = (hip_l + hip_r) / 2

            anglelist[0].append(calculate_angle(knee_r, hip_r, ankle_r))
            anglelist[1].append(calculate_angle(knee_l, hip_l, ankle_l))
            anglelist[2].append(calculate_angle(center_torso, upper_torso, bottom_torso))
            anglelist[3].append(calculate_angle(bottom_torso, upper_torso, center_ground))
            anglelist[4].append(calculate_angle(center_knee, center_hip, center_ground))

        y = count + 410
        x = np.linspace(0, 100, len(data))
        plt.figure(fig, figsize=(6, 9))
        plt.subplot(y)
        plt.plot(x, anglelist[2], label="Spine")
        plt.plot(x, anglelist[3], label="Hip")
        plt.plot(x, anglelist[4], label="Knee")
        plt.ylabel("Angle of joint")

        if count == 1:
            plt.title("Plot of Joint Angles against Frames for Different Outputs")
        if count == 4:
            plt.xlabel("Frames")
            plt.legend()

    plt.show()

############################################################
# This if-condition is True if this file was executed directly.
# It's False if this file was executed indirectly, e.g. as part
# of an import statement.
if __name__ == "__main__":
    main()