import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';



@IonicPage()
@Component({
  selector: 'page-info',
  templateUrl: 'info.html',
})
export class InfoPage {
  grab:any;
  constructor(public navCtrl: NavController, public navParams: NavParams, public http:Http) {

  }

  ionViewDidLoad() {
   this.loadGrab();
  }


  loadGrab(){
    this.http.get("https://kennynkm.com/cityhack/grab.php").map(resp=>resp.json()).subscribe(
      data =>{
        this.grab = data;
        console.log(data);
      }
    )
  }

}
