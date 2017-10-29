import { Component, ViewChild, ElementRef } from '@angular/core';
import { IonicPage, NavController, NavParams ,ToastController} from 'ionic-angular';
import { InfoPage } from '../info/info';
import { LocationTrackerProvider } from '../../providers/location-tracker/location-tracker';
/**
 * Generated class for the ReportPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */
declare var google:any;

@IonicPage()
@Component({
  selector: 'page-report',
  templateUrl: 'report.html',
})
export class ReportPage {

  @ViewChild('map') mapRef : ElementRef;
  flag:any=false;
  intervaltask:any;
  constructor(public toastCtrl: ToastController,public locationTracker: LocationTrackerProvider,public navCtrl: NavController, public navParams: NavParams) {
  
  }

  ionViewDidLoad() {
    this.showMap();
    console.log('ionViewDidLoad ReportPage');
    console.log(this.mapRef);

     var marker, i;

  
  }

  showMap(){
    const location = new google.maps.LatLng(51.507351 , -0.127758);

    const options = {
      center: location,
      zoom: 15,
      streetViewControl: false,
      mapTypeId:'roadmap'
    };
     const map = new google.maps.Map(this.mapRef.nativeElement,options);

      this.addMarker(location,map);
  }

    addMarker(position,map){
      const marker =  new google.maps.Marker({
        position,
        map
      })

    }


    doRealtime(){
      this.intervaltask = setInterval(()=>{
        this.start();
      },3000);
    }


    start(){
      
      console.log(this.locationTracker);
    var coord = new google.maps.LatLng(this.locationTracker.lat , this.locationTracker.lng);
    const options = {
      center: coord,
      zoom: 15,
      streetViewControl: false,
      mapTypeId:'roadmap'
    };
  
    const map = new google.maps.Map(this.mapRef.nativeElement,options);
    this.addMarker(coord,map);
   this.locationTracker.startTracking();

 

    if(this.flag == false){
       this.toaststart();
      this.flag = true;
        this.doRealtime();
      }
  }
 
  stop(){
    this.flag = false;
    clearInterval(this.intervaltask);
    this.locationTracker.stopTracking();
    this.toastend();
  }


  toaststart(){
const toast = this.toastCtrl.create({
    message: 'SOS Initiated',
    duration: 3000,
    position: 'top'
  });

  toast.onDidDismiss(() => {
    console.log('Dismissed toast');
  });

  toast.present();
  }

  toastend(){
const toast = this.toastCtrl.create({
    message: 'SOS Ended',
    duration: 3000,
    position: 'top'
  });

  toast.onDidDismiss(() => {
    console.log('Dismissed toast');
  });

  toast.present();
  }

initiateInfo(){
  this.navCtrl.push(InfoPage);
}  
}
