#!/bin/bash 

# Javadoc executable to use
javadocExec="javadoc"

# Set dirs
cmdDir=$(dirname $0)
baseDir="${cmdDir}/.."
javaDir="${baseDir}/android/java"
javaGenDir="${baseDir}/generated/android-java/proxies"
javadocDir="${baseDir}/dist/android/javadoc"
tempDir="${baseDir}/build/javadoc"

# Remove old temp
rm -rf ${tempDir}

# Copy java files, remove *JNI.java files
mkdir -p ${tempDir}
cp -r ${javaDir}/* ${tempDir}
cp -r ${javaGenDir}/* ${tempDir}
find ${tempDir} -name "*BaseMapView.java" -exec rm {} \;
find ${tempDir} -name "*JNI.java" -exec rm {} \;
find ${tempDir} -name "*RedrawRequestListener.java" -exec rm {} \;
find ${tempDir} -name "*ConfigChooser.java" -exec rm {} \;
find ${tempDir} -name "*AndroidUtils.java" -exec rm {} \;
find ${tempDir} -name "*LicenseType.java" -exec rm {} \;
find ${tempDir} -name "*.java" > ${tempDir}/files

# Execute JavaDoc
rm -rf ${javadocDir}
mkdir -p ${javadocDir}
${javadocExec} -classpath "${ANDROID_HOME}/platforms/android-8/android.jar" -source 1.6 -d ${javadocDir} -doctitle "CARTO Mobile SDK for Android" "@${tempDir}/files"

# Finished
echo "Done!"
