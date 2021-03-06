import os
import argparse
import string
from build.sdk_build_utils import *

ANDROID_ABIS = ['armeabi', 'armeabi-v7a', 'x86', 'arm64-v8a', 'x86_64']
IOS_ARCHS = ['i386', 'x86_64', 'armv7', 'arm64']

DEFAULT_XBUILD = 'msbuild'

def xbuild(args, dir, *cmdArgs):
  return execute(args.xbuild, dir, *cmdArgs)
	
def nuget(args, dir, *cmdArgs):
  return execute(args.nuget, dir, *cmdArgs)

def buildAndroidSO(args, abi):
  version = getVersion(args.buildnumber) if args.configuration == 'Release' else 'Devel'
  baseDir = getBaseDir()
  buildDir = getBuildDir('xamarin_android', abi)
  defines = ["-D%s" % define for define in args.defines.split(';') if define]
  options = ["-D%s" % option for option in args.cmakeoptions.split(';') if option]

  if not cmake(args, buildDir, options + [
    '-DCMAKE_TOOLCHAIN_FILE=%s/scripts/android-cmake/android.toolchain.cmake' % baseDir,
    '-DANDROID_NDK=%s' % args.androidndkpath,
    '-DCMAKE_BUILD_TYPE=%s' % args.configuration,
    '-DWRAPPER_DIR=%s' % ('%s/generated/android-csharp/wrappers' % baseDir),
    "-DANDROID_ABI='%s'" % abi,
    "-DANDROID_NATIVE_API_LEVEL='%s'" % ('android-21' if '64' in abi else 'android-9'),
    "-DSDK_CPP_DEFINES=%s" % " ".join(defines),
    "-DSDK_VERSION='%s'" % version,
    "-DSDK_PLATFORM='Xamarin Android'",
    '%s/scripts/build' % baseDir
  ]):
    return False
  return cmake(args, buildDir, [
    '--build', '.', '--', '-j4'
  ])

def buildIOSLib(args, arch):
  version = getVersion(args.buildnumber) if args.configuration == 'Release' else 'Devel'
  platform = 'OS' if arch.startswith('arm') else 'SIMULATOR'
  baseDir = getBaseDir()
  buildDir = getBuildDir('xamarin_ios', '%s-%s' % (platform, arch))
  defines = ["-D%s" % define for define in args.defines.split(';') if define]
  options = ["-D%s" % option for option in args.cmakeoptions.split(';') if option]

  if not cmake(args, buildDir, options + [
    '-G', 'Xcode',
    '-DCMAKE_TOOLCHAIN_FILE=%s/scripts/ios-cmake/iOS.cmake' % baseDir,
    '-DIOS_PLATFORM=%s' % platform,
    '-DWRAPPER_DIR=%s' % ('%s/generated/ios-csharp/wrappers' % baseDir),
    '-DINCLUDE_OBJC:BOOL=OFF',
    '-DSINGLE_LIBRARY:BOOL=ON',
    '-DENABLE_BITCODE:BOOL=OFF',
    '-DCMAKE_OSX_ARCHITECTURES=%s' % arch,
    '-DCMAKE_BUILD_TYPE=%s' % args.configuration,
    "-DSDK_CPP_DEFINES=%s" % " ".join(defines),
    "-DSDK_VERSION='%s'" % version,
    "-DSDK_PLATFORM='Xamarin iOS'",
    '%s/scripts/build' % baseDir
  ]):
    return False
  return cmake(args, buildDir, [
    '--build', '.',
    '--config', args.configuration
  ])

def buildIOSFatLib(args, archs):
  platformArchs = [('OS' if arch.startswith('arm') else 'SIMULATOR', arch) for arch in archs]
  baseDir = getBaseDir()
  buildDir = getBuildDir('xamarin_ios_unified')

  return execute('lipo', baseDir,
    '-output', '%s/libcarto_mobile_sdk.a' % buildDir,
    '-create', *["%s/%s-%s/libcarto_mobile_sdk.a" % (getBuildDir('xamarin_ios', '%s-%s' % (platform, arch)), args.configuration, 'iphoneos' if arch.startswith("arm") else "iphonesimulator") for platform, arch in platformArchs]
  )

def buildXamarinDLL(args, target):
  baseDir = getBaseDir()
  buildDir = getBuildDir('xamarin_%s' % target)
  distDir = getDistDir('xamarin')

  with open('%s/scripts/xamarin/CartoMobileSDK.%s.csproj.template' % (baseDir, target), 'r') as f:
    csProjFile = string.Template(f.read()).safe_substitute({ 'baseDir': baseDir, 'buildDir': buildDir, 'distDir': "%s/bin" % buildDir })
  with open('%s/CartoMobileSDK.%s.csproj' % (buildDir, target), 'w') as f:
    f.write(csProjFile)

  if args.xbuild is None:
    print '%s solution is in %s, please use Xamarin IDE to compile target DLL' % (target, buildDir)
    return True
    
  if not xbuild(args, buildDir,
    '/t:Build',
    '/p:Configuration=%s' % args.configuration,
    '/p:AndroidSdkDirectory=%s' % args.androidsdkpath,
    '%s/CartoMobileSDK.%s.csproj' % (buildDir, target)
  ):
    return False
  return makedirs(distDir) and \
    copyfile('%s/bin/%s/CartoMobileSDK.%s.dll' % (buildDir, args.configuration, target), '%s/CartoMobileSDK.%s.dll' % (distDir, target)) and \
    copyfile('%s/bin/%s/CartoMobileSDK.%s.xml' % (buildDir, args.configuration, target), '%s/CartoMobileSDK.%s.xml' % (distDir, target))

def buildXamarinNuget(args, target):
  baseDir = getBaseDir()
  buildDir = getBuildDir('xamarin_nuget')
  distDir = getDistDir('xamarin')
  version = args.buildversion

  with open('%s/extensions/scripts/xamarin/CartoMobileSDK.%s.nuspec.template' % (baseDir, target), 'r') as f:
    nuspecFile = string.Template(f.read()).safe_substitute({ 'baseDir': baseDir, 'buildDir': buildDir, 'configuration': args.configuration, 'nativeConfiguration': args.nativeconfiguration, 'version': version })
  with open('%s/CartoMobileSDK.%s.nuspec' % (buildDir, target), 'w') as f:
    f.write(nuspecFile)

  if not nuget(args, buildDir,
    'pack',
    '%s/CartoMobileSDK.%s.nuspec' % (buildDir, target),
    '-BasePath', '/'
  ):
    return False

  if not copyfile('%s/CartoMobileSDK.%s.%s.nupkg' % (buildDir, target, version), '%s/CartoMobileSDK.%s.%s.nupkg' % (distDir, target, version)):
    return False
  print "Output available in:\n%s\n\nTo publish, use:\nnuget push %s/CartoMobileSDK.%s.%s.nupkg -Source https://www.nuget.org/api/v2/package\n" % (distDir, distDir, target, version)
  return True

parser = argparse.ArgumentParser()
parser.add_argument('--profile', dest='profile', default='standard', type=validProfile, help='Build profile')
parser.add_argument('--defines', dest='defines', default='', help='Defines for compilation')
parser.add_argument('--xbuild', dest='xbuild', default='xbuild', help='Xamarin xbuild executable')
parser.add_argument('--nuget', dest='nuget', default='nuget', help='nuget executable')
parser.add_argument('--android-ndk-path', dest='androidndkpath', default='auto', help='Android NDK path')
parser.add_argument('--android-sdk-path', dest='androidsdkpath', default='auto', help='Android SDK path')
parser.add_argument('--cmake', dest='cmake', default='cmake', help='CMake executable')
parser.add_argument('--cmake-options', dest='cmakeoptions', default='', help='CMake options')
parser.add_argument('--configuration', dest='configuration', default='Release', choices=['Release', 'Debug'], help='Configuration')
parser.add_argument('--build-number', dest='buildnumber', default='', help='Build sequence number, goes to version str')
parser.add_argument('--build-version', dest='buildversion', default='%s-devel' % SDK_VERSION, help='Build version, goes to distributions')
parser.add_argument('--build-nuget', dest='buildnuget', default=False, action='store_true', help='Build Nuget package')
parser.add_argument(dest='target', choices=['android', 'ios'], help='Target platform')

args = parser.parse_args()
if args.xbuild == 'auto':
  args.xbuild = DEFAULT_XBUILD
elif args.xbuild == 'none':
  args.xbuild = None
if args.androidsdkpath == 'auto' and args.target == 'android':
  args.androidsdkpath = os.environ.get('ANDROID_HOME', None)
  if args.androidsdkpath is None:
    print "ANDROID_HOME variable not set"
    exit(-1)
if args.androidndkpath == 'auto' and args.target == 'android':
  args.androidndkpath = os.environ.get('ANDROID_NDK_HOME', None)
  if args.androidndkpath is None:
    args.androidndkpath = os.path.join(args.androidsdkpath, 'ndk-bundle')
args.defines += ';' + getProfile(args.profile).get('defines', '')
args.defines += ';TARGET_XAMARIN'
args.cmakeoptions += ';' + getProfile(args.profile).get('cmake-options', '')
args.nativeconfiguration = args.configuration

target = None
if args.target == 'android':
  target = 'Android'
  for abi in ANDROID_ABIS:
    if not buildAndroidSO(args, abi):
      exit(-1)
elif args.target == 'ios':
  target = 'iOS'
  for arch in IOS_ARCHS:
    if not buildIOSLib(args, arch):
      exit(-1)
  if not buildIOSFatLib(args, IOS_ARCHS):
    exit(-1)

if not buildXamarinDLL(args, target):
  exit(-1)

if args.buildnuget:
  if not buildXamarinNuget(args, target):
    exit(-1)
