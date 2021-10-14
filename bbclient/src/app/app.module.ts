import {LOCALE_ID, NgModule} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from "@angular/forms";
import { HttpClientModule } from "@angular/common/http";
import { registerLocaleData } from "@angular/common";
import localeRu from '@angular/common/locales/ru'
import localeRuExtra from '@angular/common/locales/extra/ru'
import { Routes } from "@angular/router";
import { RouterModule } from "@angular/router";

import { AppComponent } from './app.component';
import { ArticleListComponent } from './article-list.component';
import { ArticleDetailComponent } from './article-detail.component';
import { ArticleService } from './article.service';

registerLocaleData(localeRu, 'ru', localeRuExtra)

const appRoutes: Routes = [
  {path: ':pk', component: ArticleDetailComponent},
  {path: '', component: ArticleListComponent},
]

@NgModule({
  declarations: [
    AppComponent,
    ArticleListComponent,
    ArticleDetailComponent
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    ArticleService,
    {provide: LOCALE_ID, useValue: 'ru'}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
