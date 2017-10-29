import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';
import { BackgroundGeolocation } from '@ionic-native/background-geolocation';
import { LocationTrackerProvider } from '../providers/location-tracker/location-tracker';
import { Geolocation } from '@ionic-native/geolocation';
import { OneSignal } from '@ionic-native/onesignal';
import { HttpModule } from '@angular/http';

import { MyApp } from './app.component';
import { HomePage } from '../pages/home/home';
import { ReportPage } from '../pages/report/report';
import { ReportPageModule } from '../pages/report/report.module';
import { InfoPage } from '../pages/info/info';
import { InfoPageModule } from '../pages/info/info.module';


@NgModule({
  declarations: [
    MyApp,
    HomePage
  ],
  imports: [
    BrowserModule,
    ReportPageModule,
    InfoPageModule,
    IonicModule.forRoot(MyApp),
    HttpModule
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    HomePage,
    ReportPage,
    InfoPage
  ],
  providers: [
    StatusBar,
    LocationTrackerProvider,
    BackgroundGeolocation,
    Geolocation,
    OneSignal ,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler}
  ]
})
export class AppModule {}
