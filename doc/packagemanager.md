# Package Manager

CARTO Mobile SDK offers a convenient way for you to manage different offline packages: map, routing and geocoding. The API is the same, no matter what kind of packages you download. The only difference is in the `source` you define.

* `carto.streets` is the base source used to download map packages
* `routing:carto.streets` for routing packages
* `geocoding:carto.streets` for geocoding packages

## Define Folder

Each type of package should be stored in a different folder, e.g. `mappackages`, `routingpackages`, `geocodingpackages`.

<div class="js-TabPanes">
  <ul class="Tabs">
    <li class="Tab js-Tabpanes-navItem--lang is-active">
      <a href="#/0" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--java">Java</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/1" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--csharp">C#</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/2" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--objective-c">Objective-C</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/3" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--swift">Swift</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/3" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--kotlin">Kotlin</a>
    </li>
  </ul>

   <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--java is-active">
  {% highlight java %}

	// Create PackageManager instance for dealing with offline packages
	File packageFolder = new File(getApplicationContext().getExternalFilesDir(null), "foldername");
	    
	if (!(packageFolder.mkdirs() || packageFolder.isDirectory())) {
	    Log.e(Const.LOG_TAG, "Could not create package folder!");
	}
	
	try {
	    packageManager = new CartoPackageManager("<your-package-source>", packageFolder.getAbsolutePath());
	} catch (IOException e) {
	    e.printStackTrace();
	}

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--csharp">
  {% highlight csharp %}
	
	// Create PackageManager instance for dealing with offline packages
	var packageFolder = new File(GetExternalFilesDir(null), "foldername");
	
	if (!(packageFolder.Mkdirs() || packageFolder.IsDirectory))
	{
		Log.Fatal("Could not create package folder!");
	}
	
	packageManager = new CartoPackageManager("<your-package-source>", packageFolder);

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--objective-c">
  {% highlight objc %}

	// Define PackageManger to download offline packages
	// Create folder for package manager. Package manager needs persistent writable folder.
	NSArray* paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory, NSUserDomainMask,YES);
	NSString* appSupportDir = [paths objectAtIndex: 0];
	NSString* packagesDir = [appSupportDir stringByAppendingString:@"/foldername"];
	NSError *error;
	[[NSFileManager defaultManager] createDirectoryAtPath:packagesDir withIntermediateDirectories:YES attributes:nil error:&error];
	    
	packageManager = [[NTCartoPackageManager alloc] initWithSource:@"<your-package-source>" dataFolder:packagesDir];

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--swift">
  {% highlight swift %}
  
        // Define PackageManger to download offline packages
        // Create folder for package manager. Package manager needs persistent writable folder.
        let packageFolder = NTAssetUtils.calculateWritablePath("foldername")
        
        do {
            try FileManager.default.createDirectory(atPath: packageFolder!, withIntermediateDirectories: false, attributes: nil)
        } catch let error as NSError {
            print(error.localizedDescription);
        }
        
        // Create PackageManager instance for dealing with offline packages
        var packageManager =  NTCartoPackageManager(source: "<your-package-source>", dataFolder: packageFolder)

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--kotlin">
  {% highlight kotlin %}
  
        // Create PackageManager instance for dealing with offline packages
        val packageFolder = File(applicationContext.getExternalFilesDir(null), "foldername")

        if (!(packageFolder.mkdirs() || packageFolder.isDirectory())) {
            println("Could not create package folder!")
        }

        var packageManager = try {
            CartoPackageManager("<your-package-source>", packageFolder.absolutePath)
        } catch (e: IOException) {
            null
        }

  {% endhighlight %}
  </div>
  
</div>
 
## PackageManagerListener Events

Package downloads cannot be started immediately, as the Mobile SDK needs to get latest definition of packages from CARTO online service. Once this list is received, PackageManagerListener's `onPackageListUpdated()` is called.

Write your own `PackageManagerListener`, and start package download using the `onPackageListUpdated` method, which ensures that the package metadata is downloaded.

<div class="js-TabPanes">
  <ul class="Tabs">
    <li class="Tab js-Tabpanes-navItem--lang is-active">
      <a href="#/0" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--java">Java</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/1" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--csharp">C#</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/2" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--objective-c">Objective-C</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/3" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--swift">Swift</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/3" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--kotlin">Kotlin</a>
    </li>
  </ul>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--java is-active">
  {% highlight java %}
  
  public class MyPackageManagerListener extends PackageManagerListener {
    @Override
    public void onPackageListUpdated() {
        Log.d(Const.LOG_TAG, "Package list updated");
        // Start download of package of Estonia
        // see list of available ID-s: https://github.com/CartoDB/mobile-sdk/wiki/List-of-Offline-map-packages
        packageManager.startPackageDownload("EE");
        packageManager.startPackageDownload("LV");
    }

    @Override
    public void onPackageListFailed() {
        Log.e(Const.LOG_TAG, "Package list update failed");
    }

    @Override
    public void onPackageStatusChanged(String id, int version, PackageStatus status)
    {
        // you can monitor download process %
    }

    @Override
    public void onPackageCancelled(String id, int version) {
    }

    @Override
    public void onPackageUpdated(String id, int version) {
        Log.d(Const.LOG_TAG, "Offline package updated: " + id);
    }

    @Override
    public void onPackageFailed(String id, int version, PackageErrorType errorType) {
        Log.e(Const.LOG_TAG, "Offline package update failed: " + id);
    }
  }

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--csharp">
  {% highlight csharp %}
  
  public class MyPackageManagerListener : PackageManagerListener
  {
    PackageManager packageManager;

    public MyPackageManagerListener(PackageManager manager)
    {
      packageManager = manager;
    }

    public override void OnPackageListUpdated()
    {
      Log.Debug("Package list updated");
      // We have packages all country/regions
      // see list of available ID-s: https://github.com/CartoDB/mobile-sdk/wiki/List-of-Offline-map-packages
      packageManager.StartPackageDownload("EE");
      packageManager.StartPackageDownload("LV");
    }

    public override void OnPackageListFailed()
    {
      Log.Error("Package list update failed");
    }

    public override void OnPackageStatusChanged(String id, int version, PackageStatus status)
    {
      // here you can get progress of download
    }

    public override void OnPackageCancelled(String id, int version)
    {
    }

    public override void OnPackageUpdated(String id, int version)
    {
      Log.Debug("Offline package updated: " + id);
    }

    public override void OnPackageFailed(String id, int version, PackageErrorType errorType)
    {
      Log.Error("Offline package download failed: " + id);
    }
  }

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--objective-c">
  {% highlight objc %}
  
  @interface MyPackageManagerListener : NTPackageManagerListener

    @property NTPackageManager* _packageManager;
  - (void)setPackageManager:(NTPackageManager*)manager;
  
  @end

  @implementation MyPackageManagerListener

  - (void)onPackageListUpdated
  {
      NSLog(@"onPackageListUpdated");
      // We have packages all country/regions
      // see list of available ID-s: https://github.com/CartoDB/mobile-sdk/wiki/List-of-Offline-map-packages
      [self._packageManager startPackageDownload: @"EE"];
      [self._packageManager startPackageDownload: @"LV"];
  }

  - (void)onPackageListFailed
  {
      NSLog(@"onPackageListFailed");
  }

  - (void)onPackageUpdated:(NSString*)packageId version:(int)version
  {
  }

  - (void)onPackageCancelled:(NSString*)packageId version:(int)version
  {
  }

  - (void)onPackageFailed:(NSString*)packageId version:(int)version errorType:(enum NTPackageErrorType)errorType
  {
      NSLog(@"onPackageFailed");
  }

  - (void)onPackageStatusChanged:(NSString*)packageId version:(int)version status:(NTPackageStatus*)status
  {
      // here you can get progress of download
      NSLog(@"onPackageStatusChanged progress: %f", [status getProgress]);
  }

  - (void)setPackageManager:(NTPackageManager*)manager
  {
      self._packageManager = manager;
  }

  @end


  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--swift">
  {% highlight swift %}
  
public class MyPackageManagerListener : NTPackageManagerListener {
    
    var packageManager: NTCartoPackageManager?
    
    convenience init(packageManager: NTCartoPackageManager) {
        self.init()
        self.packageManager = packageManager
    }
    
    public override func onPackageListUpdated() {
        
        // Start download of package of Estonia & Latvia
        // see list of available ID-s: https://github.com/CartoDB/mobile-sdk/wiki/List-of-Offline-map-packages
        self.packageManager?.startPackageDownload("EE");
        self.packageManager?.startPackageDownload("LV");
    }
    
    public override func onPackageListFailed() {
        
    }
    
    public override func onPackageStatusChanged(_ arg1: String!, version: Int32, status: NTPackageStatus!) {
        // Here you can monitor download process %
    }
    public override func onPackageUpdated(_ arg1: String!, version: Int32) {
        
    }
    
    public override func onPackageCancelled(_ arg1: String!, version: Int32) {
        
    }
    
    public override func onPackageFailed(_ arg1: String!, version: Int32, errorType: NTPackageErrorType) {
        
    }
}

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--kotlin">
  {% highlight kotlin %}
  
    class MyPackageManagerListener(val packageManager: CartoPackageManager) : PackageManagerListener() {

        override fun onPackageListUpdated() {

            // Start download of package of Estonia & Latvia
            // see list of available ID-s: https://github.com/CartoDB/mobile-sdk/wiki/List-of-Offline-map-packages
            packageManager.startPackageDownload("EE");
            packageManager.startPackageDownload("LV");
        }

        override fun onPackageListFailed() {

        }

        override fun onPackageStatusChanged(id: String?, version: Int, status: PackageStatus?) {
            // Here you can monitor download process %
        }

        override fun onPackageUpdated(id: String?, version: Int) {

        }

        override fun onPackageCancelled(id: String?, version: Int) {

        }

        override fun onPackageFailed(id: String?, version: Int, errorType: PackageErrorType?) {

        }
    }

  {% endhighlight %}
  </div>
    
</div>

**Note:** If you are wondering why these code samples include `EE` and `LV` (Estonia and Latvia) packages, see why [these countries might be linked](http://www.baltictimes.com/estonian_president_marries_latvian_cyber_defence_expert/). This shows that offline works across borders.

## Initialize PackageManager

To link PackageManagerListener with PackageManager, apply the following code.

<div class="js-TabPanes">
  <ul class="Tabs">
    <li class="Tab js-Tabpanes-navItem--lang is-active">
      <a href="#/0" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--java">Java</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/1" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--csharp">C#</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/2" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--objective-c">Objective-C</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/3" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--swift">Swift</a>
    </li>
    <li class="Tab js-Tabpanes-navItem--lang">
      <a href="#/3" class="js-Tabpanes-navLink--lang js-Tabpanes-navLink--lang--kotlin">Kotlin</a>
    </li>
  </ul>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--java is-active">
  {% highlight java %}

// 1. Set listener, and start PackageManager
 packageManager.setPackageManagerListener(new MyPackageManagerListener());
 packageManager.start();

// 2. Fetch list of available packages from server. Note that this is asynchronous operation and listener will be notified via onPackageListUpdated when this succeeds.
 packageManager.startPackageListDownload();

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--csharp">
  {% highlight csharp %}

// 1. Create and set listener, and start PackageManager
 packageManager.PackageManagerListener = new MyPackageManagerListener(packageManager);
 packageManager.Start();

// 2. Fetch list of available packages from server. 
 // Note that this is asynchronous operation and the listener will be notified via OnPackageListUpdated when this succeeds.        
 packageManager.StartPackageListDownload();

  {% endhighlight %}
  </div>

   <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--objective-c">
  {% highlight objc %}
  
	NTCartoPackageManager* packageManager = [[NTCartoPackageManager alloc] initWithSource:@"<your-package-source>" dataFolder:packagesDir];
	    
// 1. Create PackageManagerListener with your listener class
MyPackageManagerListener* _packageManagerListener = [[MyPackageManagerListener alloc] init];
[_packageManagerListener setPackageManager: packageManager];
    
// Attach package manager listener
[packageManager setPackageManagerListener:_packageManagerListener];
    
// Start PackageManager
[packageManager start];
    
// 2. Start download of packageList. When download is done, then the listener's onPackageListUpdated() is called
[packageManager startPackageListDownload];

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--swift">
  {% highlight swift %}
  
// Create PackageManager instance for dealing with offline packages
var packageManager =  NTCartoPackageManager(source: "<your-package-source>", dataFolder: packageFolder)
    
// 1. Set listener, and start PackageManager
packageManager?.setPackageManagerListener(MyPackageManagerListener(packageManager: packageManager!))
packageManager?.start()
    
// 2. Fetch list of available packages from server.
// Note that this is asynchronous operation
// and listener will be notified via onPackageListUpdated when this succeeds.
packageManager?.startPackageListDownload()

  {% endhighlight %}
  </div>

  <div class="Carousel-item js-Tabpanes-item--lang js-Tabpanes-item--lang--kotlin">
  {% highlight kotlin %}
  
// 1. Set listener, and start PackageManager
packageManager?.packageManagerListener = MyPackageManagerListener(packageManager!!)
packageManager.start()

// 2. Fetch list of available packages from server. 
// Note that this is asynchronous operation 
// and listener will be notified via onPackageListUpdated when this succeeds.
packageManager.startPackageListDownload()

  {% endhighlight %}
  </div>
    
</div>

## Bounding Box

CARTO Mobile SDK allows for the download of custom areas, called bounding boxes. It can be anything from a park, a city, a route, or a block of countries.

A bounding box is constructed as `bbox(min-longitude,min-latitude,max-longitude,max-latitude`, so the bounding box of Berlin would be: `bbox(13.2285,52.4698,13.5046,52.57477)`. This is used as the package **id** instead of a country or county code.

An example of a custom BoundingBox (written in Kotlin) class is available [here](https://github.com/CartoDB/mobile-android-samples/blob/master/AdvancedMapKotlin/app/src/main/java/com/carto/advanced/kotlin/utils/BoundingBox.kt) and implementation can be seen [here](https://github.com/CartoDB/mobile-android-samples/blob/AdvancedMapKotlin/AdvancedMapKotlin/app/src/main/java/com/carto/advanced/kotlin/model/Cities.kt).
