import {Component, inject, OnInit} from '@angular/core';
import {ApiService} from "./api.service";
import {repeat} from "rxjs";

export type queueItem = {
  data: number
  timestamp: number
}
type queueItem2 = {
  type: number
  count: number
  lastTimestamp: number
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  title = 'diy-app';
  api = inject(ApiService)
  queue: queueItem2[] = []
  threshold = 60 * 1000

  icons: { [index: number]: string } = {
    1: "question_mark",
    2: "volume_up",
    3: "question_exchange",
    4: "swipe_up",
    5: "replay"
  }

  ngOnInit() {
    this.icons = {
      1: "1",
      2: "2",
      3: "3",
      4: "4",
      5: "5"
    }
    this.api.getQueue().pipe(repeat({
      delay: 500,
    })).subscribe(
      (queue) => {
        console.log("GOT NET QUEUE", queue)
        this.queue = []
        const currentTime = new Date().getTime() - new Date().getTimezoneOffset()* 60000
        queue.map((item)=>{
          if (currentTime > item.timestamp + this.threshold) return
          const x = this.queue.find((item2 ) => item.data === item2.type)
          if (x){
            x.count +=1
            x.lastTimestamp = Math.max(x.lastTimestamp, item.timestamp)
          }else {
            this.queue.push({
              type: item.data,
              count: 1,
              lastTimestamp: item.timestamp
            })
          }
          console.log("QUEUE LENGTH", this.queue.length)
        })
      }
    )
  }

  getIcon(n: number){
    return this.icons[n];
  }

  onThresholdChange(value: string){
    this.threshold = Number(value) * 1000
    console.log(this.threshold)
  }

  onClearQueue(){
    this.api.clearQueue().subscribe()
  }
}
