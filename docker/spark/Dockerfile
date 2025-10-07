FROM openjdk:11-jre-slim

# Install Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Spark
ENV SPARK_VERSION=3.4.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark

RUN wget -q https://archive.apache.org/dist/spark/spark-/spark--bin-hadoop.tgz && \
    tar -xzf spark--bin-hadoop.tgz && \
    mv spark--bin-hadoop  && \
    rm spark--bin-hadoop.tgz

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

# Set environment variables
ENV PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Users/Moe_k/.local/bin:/mnt/c/Python313/Scripts/:/mnt/c/Python313/:/mnt/c/Python312:/mnt/c/Python312/Scripts:/mnt/c/Program Files/Python310/Scripts/:/mnt/c/Program Files/Python310/:/mnt/c/Users/Moe_k/AppData/Local/Programs/cursor/resources/app/bin:/mnt/c/Program Files/Microsoft SDKs/Azure/CLI2/wbin:/mnt/c/Program Files (x86)/VMware/VMware Player/bin/:/mnt/c/Program Files/Common Files/Oracle/Java/javapath:/mnt/c/Program Files/OpenLogic/jre-8.0.372.07-hotspot/bin:/mnt/c/Program Files (x86)/Common Files/Intel/Shared Libraries/redist/intel64/compiler:/mnt/c/Windows/system32:/mnt/c/Windows:/mnt/c/Windows/System32/Wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0/:/mnt/c/Windows/System32/OpenSSH/:/mnt/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/mnt/c/WINDOWS/system32:/mnt/c/WINDOWS:/mnt/c/WINDOWS/System32/Wbem:/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/:/mnt/c/WINDOWS/System32/OpenSSH/:/mnt/c/xampp/php:/mnt/c/ProgramData/ComposerSetup/bin:/mnt/c/Program Files (x86)/Microsoft SQL Server/160/Tools/Binn/:/mnt/c/Program Files/Microsoft SQL Server/160/Tools/Binn/:/mnt/c/Program Files/Micr:/mnt/c/Program Files/Neovim/bin:/mnt/c/Program Files/do:/mnt/c/Python312/Scripts:/mnt/c/Python312:/mnt/c/Users/Moe_k/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/Moe_k/AppData/Local/Programs/Microsoft VS Code/bin:/mnt/c/Users/Moe_k/AppData/Roaming/Composer/vendor/bin:/mnt/c/Program Files/Azure Data Studio/bin:/mnt/c/Users/Moe_k/AppData/Local/GitHubDesktop/bin:/mnt/c/Users/Moe_k/AppData/Roaming/nvm:/mnt/c/Program Files/nodejs:/mnt/c/Program Files/JetBrains/IntelliJ IDEA Community Edition 2023.3.4/bin:/mnt/c/Program Files/JetBrains/IntelliJ IDEA 2024.1/bin:/mnt/c/Users/Moe_k/.dotnet/tools:/mnt/c/Program Files/curl-8.7.1_9-win64-mingw/bin:/mnt/c/Program Files/PostgreSQL/16/bin:/mnt/c/Users/Moe_k/AppData/Local/Programs/mongosh/:/mnt/c/Program Files/apache-maven-3.9.9/bin:/mnt/c/Program Files/terraform_1.10.2_windows_amd64:/mnt/c/Users/Moe_k/go/bin:/mnt/c/Users/Moe_k/AppData/Local/Programs/Windsurf/bin:/mnt/c/flutter/src/flutter/bin:/mnt/c/Program Files/Git/bin:/mnt/c/Users/Moe_k/AppData/Local/Programs/cursor/resources/app/bin:/Docker/host/bin:/mnt/c/Program Files/ripgrep-13.0.0-x86_64-pc-windows-msvc:/mnt/c/ProgramData/chocolatey/bin:/mnt/c/Users/Moe_k/AppData/Local/Programs/Ollama:/mnt/c/Users/Moe_k/AppData/Roaming/npm:/mnt/c/hadoop/hadoop-3.4.1/bin:/mnt/c/Program Files/Java/jdk-25/bin:/mnt/c/Users/Moe_k/.cursor/extensions/ms-python.debugpy-2025.10.0-win32-x64/bundled/scripts/noConfigScripts
ENV PYTHONPATH=/python:/python/lib/py4j-0.10.9.5-src.zip:

# Copy application code
COPY spark_jobs/ /opt/spark_jobs/

WORKDIR /opt/spark_jobs

EXPOSE 8080 7077 6066

CMD ["/opt/spark/bin/spark-class", "org.apache.spark.deploy.master.Master"]

