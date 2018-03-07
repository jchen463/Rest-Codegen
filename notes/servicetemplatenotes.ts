
// REQUIRED PARAMETERS CHECK
if (petId === null || petId === undefined) {
    throw new Error('Required parameter petId was null or undefined when calling getPetById.');
}

// INCLUDED IN EVERY FUNCTION HARD CODED
let headers = this.defaultHeaders;

// AUTHENTIFICATION

// to determine the Accept header
// UNSURE ON CONDITION
let httpHeaderAccepts: string[] = [
    'application/json',
    'application/xml'
];

// INCLUDED IN EVERY FUNCTION HARD CODED
let httpHeaderAcceptSelected: string = this.configuration.selectHeaderAccept(httpHeaderAccepts);
if (httpHeaderAcceptSelected != undefined) {
    headers = headers.set("Accept", httpHeaderAcceptSelected);
}

// to determine the Content-Type header
// REQUEST BODY
let consumes: string[] = [
];

// UNSURE ON CONDITION addPet updatePet placeOrder updateUser createUser createUsersWithArrayInput
// post and put
let httpContentTypeSelected: string = this.configuration.selectHeaderContentType(consumes);
if (httpContentTypeSelected != undefined) {
    headers = headers.set("Content-Type", httpContentTypeSelected);
}

// INCLUDED IN EVERY FUNCTION. 
// UNSURE ON CONDITION
return this.httpClient.get<any>(`${this.basePath}/pet/${encodeURIComponent(String(petId))}`,
{
    headers: headers,
    withCredentials: this.configuration.withCredentials,
}
);

// IN: QUERY . ALSO DEPENDENT ON TYPE OF PARAM?
let queryParameters = new HttpParams({encoder: new CustomHttpUrlEncodingCodec()});
if (username !== undefined) {
    queryParameters = queryParameters.set('username', <any>username);
}
if (password !== undefined) {
    queryParameters = queryParameters.set('password', <any>password);
}

let queryParameters = new HttpParams({ encoder: new CustomHttpUrlEncodingCodec() });
if (tags) {
    tags.forEach((element) => {
        queryParameters = queryParameters.append('tags', <any>element);
    })
}