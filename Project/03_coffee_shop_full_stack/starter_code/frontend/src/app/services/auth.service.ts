import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';

import { environment } from '../../environments/environment';

const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';
const JWTS_ACTIVE_INDEX_KEY = 'JWTS_ACTIVE_INDEX_KEY';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  url = environment.auth0.url;
  audience = environment.auth0.audience;
  clientId = environment.auth0.clientId;
  callbackURL = environment.auth0.callbackURL;
  
  jwtToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5kQ3I4bFU4UzJvRVk2X3c1TjNDeSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQwMDEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyYmI4OGQ5OGVjZTU0ZjU3MzdhM2Q1MCIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTY1NjQ1ODcxNywiZXhwIjoxNjU2NDY1OTE3LCJhenAiOiI4QktsWFc2SVJvRnUyZDJ0anVFMTdCdHlHR1ZHbnR6YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIl19.SmpOsECHMLNgleY_qQBr8r--njy3X5kF2MDn3VeEVWL5GlxOX1HabMA-2v9muGyVaaP7P7exF4c7P0EEE5UkyWw-IrB-TJn90VICb-adlIbSUHC7txt4G1TjjQnuHgPgn_KQZZ9FRar38zf7LkfGooi2XBwXYAVxDUPepftrirBQ9aAvXNcuilkj0fgbcwT1ycrUtBQKFjAYy0NChLBwrQJxvgS66xAGjrxdw-esTsHYVeZOOYVLTQRG-lEz57XYGIN2fPYF_XJyeCSbfz-tSp1NLF_JXFF0beS8MNmNJAHsGO_LU2sJHAOwaBRNCdMuHqdlqoQI4TqvxBIrWEku6A'


  token: string;
  payload: any;

  constructor() { }

  build_login_link(callbackPath = '') {
    let link = 'https://';
    link += this.url + '.auth0.com';
    link += '/authorize?';
    link += 'audience=' + this.audience + '&';
    link += 'response_type=token&';
    link += 'client_id=' + this.clientId + '&';
    link += 'redirect_uri=' + this.callbackURL + callbackPath;
    return link;
  }

  // invoked in app.component on load
  check_token_fragment() {
    // parse the fragment
    const fragment = window.location.hash.substr(1).split('&')[0].split('=');
    // check if the fragment includes the access token
    if ( fragment[0] === 'access_token' ) {
      // add the access token to the jwt
      this.token = fragment[1];
      // save jwts to localstore
      this.set_jwt();
    }
  }

  set_jwt() {
    localStorage.setItem(JWTS_LOCAL_KEY, this.token);
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  load_jwts() {
    this.token = localStorage.getItem(JWTS_LOCAL_KEY) || null;
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  activeJWT() {
    return this.token;
  }

  decodeJWT(token: string) {
    const jwtservice = new JwtHelperService();
    this.payload = jwtservice.decodeToken(token);
    return this.payload;
  }

  logout() {
    this.token = '';
    this.payload = null;
    this.set_jwt();
  }

  can(permission: string) {
    return this.payload && this.payload.permissions && this.payload.permissions.length && this.payload.permissions.indexOf(permission) >= 0;
  }
}
