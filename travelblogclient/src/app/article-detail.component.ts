import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";

import {ArticleService} from "./article.service";

@Component({
  selector: 'app-article-detail',
  templateUrl: './article-detail.component.html',
  styleUrls: ['./article-detail.component.css']
})
export class ArticleDetailComponent implements OnInit {
  article: any;
  comments: any;
  author: String = '';
  password: String = '';
  content: String = '';

  constructor(private articleservice: ArticleService, private ar: ActivatedRoute) { }

  ngOnInit() {
    const pk = this.ar.snapshot.params.pk;
    this.articleservice.getArticle(pk).subscribe((article: Object) => {
      this.article = article;
      this.getComments();
    })
  }

  getComments() {
    this.articleservice.getComments(this.article.id).subscribe(
      (comments: Object[]) => {this.comments = comments;}
    );
  }

  submitComment() {
    this.articleservice.addComment(this.article.id, this.author, this.password, this.content).subscribe(
      (comment: Object) => {
        if (comment) {
          this.content = '';
          this.getComments();
        }
      }
    )
  }

}
