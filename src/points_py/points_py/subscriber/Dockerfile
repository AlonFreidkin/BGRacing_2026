FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy
RUN apt update && apt install -y\
    locales \
    software-properties-common \
    curl \ 
    wget \
    gnupg2 \
    build-essential \
    git \
    python3-pip \
    python3.12 \
    python3.12-venv \
    # Add other common build tools if needed
    && rm -rf /var/lib/apt/lists/*
RUN apt update && apt install git curl wget net-tools iputils-ping iproute2 -y
RUN locale-gen en_US en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Add ROS 2 apt repository
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update apt and install ROS 2 Jazzy desktop full
RUN apt update && apt install -y \
    ros-$ROS_DISTRO-desktop-full \
    # Install any additional Python packages required for ROS 2 or your project
    && rm -rf /var/lib/apt/lists/*

# Source ROS 2 setup file
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc

# Set Python 3.12 as the default python for system
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Install pip for Python 3.12
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

    # Activate the virtual environment and install packages
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /tmp/requirements.txt
COPY subscriber_s.py .
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN useradd -m devuser
WORKDIR /home/devuser
USER devuser
ENV VAR=13
CMD ["bash"]
