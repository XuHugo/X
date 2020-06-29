

export  function arequest(url, data, type){
	console.log("arequest ")
	fetch(url ,{
		method: type,
		headers:{
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		credentials: 'include',
		body:JSON.stringify(data)
	})
	.then(function(response){
		console.log(response.json());
		return response.json();
	})
	.then(function (jsonData) {
		console.log(jsonData);
	})
	.catch(function (){
		console.log("request error!!!")
	})
}

export default async function request(url, data, type){
	console.log("request ",url)
	let ret = await fetch(url ,{
		method: type,
		headers:{
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		credentials: 'include',
		body:JSON.stringify(data)
	})

	ret = await ret.json()
	return ret
}

