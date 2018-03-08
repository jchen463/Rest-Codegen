// to determine the Accept header
// UNSURE ON CONDITION - RESPONSES -> IF 'CONTENT' NOT INCLUDED, DEFAULTS TO THESE TWO
// IF 'CONTENT' IS PRESENT, ONLY LISTS THE FIELDS UNDER 'CONTENT'
let httpHeaderAccepts: string[] = [
    'application/json',
    'application/xml'
];

// INCLUDED IN EVERY FUNCTION. 
// UNSURE ON CONDITION
return this.httpClient.get<any>(`${this.basePath}/pet/${encodeURIComponent(String(petId))}`,
    {
        headers: headers,
        withCredentials: this.configuration.withCredentials,
    }
);




// IN: PATH
convertFormParamsToString ? formParams.toString() : formParams, 

// IN: QUERY
params: queryParameters,

// to determine the Content-Type header
// REQUEST BODY
let consumes: string[] = [
];

// addPet updatePet placeOrder updateUser createUser createUsersWithArrayInput
// post and put
let httpContentTypeSelected: string = this.configuration.selectHeaderContentType(consumes);
if (httpContentTypeSelected != undefined) {
    headers = headers.set("Content-Type", httpContentTypeSelected);
}


// IN: QUERY . ALSO DEPENDENT ON TYPE OF PARAM
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