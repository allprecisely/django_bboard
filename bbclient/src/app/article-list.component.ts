import { Component, OnInit } from '@angular/core';

import {ArticleService} from "./article.service";

@Component({
  selector: 'app-article-list',
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.css']
})
export class ArticleListComponent implements OnInit {
  articles: any;

  constructor(private articleservice: ArticleService) { }

  ngOnInit() {
    this.articleservice.getArticles().subscribe(
      (articles: Object[]) => {this.articles = articles; console.warn(articles);}
    );
  }

}
