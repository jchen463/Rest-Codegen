// STILL NOT SURE ON THIS CONDITION
{% if CONDITION%}
const canConsumeForm = this.canConsumeForm(consumes);

let formParams: { append(param: string, value: any): void; };
let useForm = false;
let convertFormParamsToString = false;
{% if CONDITION %}
useForm = canConsumeForm;
{% endif %}
if (useForm) {
    formParams = new FormData();
} else {
    formParams = new HttpParams({ encoder: new CustomHttpUrlEncodingCodec() });
}
{% for param in path['properties'].parameters %}
if ({{param.name}} !== undefined) {
    formParams = formParams.append('{{param.name}}', <any>{{param.name}}) || formParams;
}
{% endfor %}
{% endif %}

// NOT SURE ON THIS CONDITION EITHER. SHOWS UP ON TWO PET FUNCTIONS
{% if path['in'] == 'path' %}
convertFormParamsToString ? formParams.toString() : formParams, 
{% endif %}

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