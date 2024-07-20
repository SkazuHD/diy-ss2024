import {inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {queueItem} from "./app.component";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = "http://192.168.4.1/"
  private http = inject(HttpClient)

  getQueue(){
    return this.http.get(this.apiUrl+"queue") as Observable<queueItem[]>
  }

  clearQueue() {
    return this.http.post(this.apiUrl+"clear", {})
  }
}
