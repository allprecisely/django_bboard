import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {catchError} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class ArticleService {
  private url: String = 'http://localhost:8000';
  constructor(private http: HttpClient) {
  }

  getArticles(): Observable<Object[]> {
    return this.http.get<Object[]>(this.url + '/api/articles/');
  }

  getArticle(pk: Number): Observable<Object> {
    return this.http.get<Object>(this.url + '/api/articles/' + pk)
  }

  handleError() {
    return (error: any): Observable<Object> => {
      window.alert(error.messages);
      // @ts-ignore
      return of(null);
    }
  }

  addComment(article: String, author: String, password: String, content: String): Observable<Object> {
    const comment = {'article': article, 'author': author, 'content': content};
    const options = {headers: new HttpHeaders(
        {'Content-Type': 'application/json',
        'Authorization': 'Basic ' + window.btoa(author + ':' + password)})};
    return this.http.post<Object>(this.url + '/api/articles/' + article + '/comments/', comment, options).pipe(
      catchError(this.handleError())
    );
  }

  getComments(pk: Number): Observable<Object[]> {
    return this.http.get<Object[]>(this.url + '/api/articles/' + pk + '/comments/');
  }

}
