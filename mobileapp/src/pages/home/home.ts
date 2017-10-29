import { Component } from '@angular/core';
import { NavController , Nav } from 'ionic-angular';
import { ReportPage } from '../report/report';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  constructor(public navCtrl: NavController, public nav: Nav) {

  }
  movetoreport(){
    this.nav.setRoot(ReportPage);
  }
}
