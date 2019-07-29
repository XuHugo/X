function select_net(nets)
{
    switch(nets)
    {
        case "main":net="https://mainnet.infura.io/xWBzBkvXjmY7vhAeUD4B";
            break;
        case "ropsten":net="https://ropsten.infura.io/xWBzBkvXjmY7vhAeUD4B";
            break;
        case "rinkeby":net="https://rinkeby.infura.io/xWBzBkvXjmY7vhAeUD4B";
            break;
        case "kovan":net="https://kovan.infura.io/xWBzBkvXjmY7vhAeUD4B";
            break;
    }
    return net
}
function generate_address(seed)
{
    if(seed == undefined)
    {
        seed=document.getElementById("seed").value;
    }

    if(seed == "")
    {
            var new_seed = lightwallet.keystore.generateRandomSeed();
            document.getElementById("seed").value = new_seed;
            seed = new_seed;
            document.getElementById("info").innerHTML="new address";
    }
    if(!lightwallet.keystore.isSeedValid(seed))
    {
        document.getElementById("info").innerHTML="invalid seed";
        return;
    }

    var password = Math.random().toString();
    var hdPath = "m/44'/60'/0'/0";
    lightwallet.keystore.createVault({
        password: password,
        seedPhrase: seed,
        hdPathString: hdPath
    },function(err, ks){
        ks.keyFromPassword(password,function(err,pwDerivedKey){
        if(err)
        {
            document.getElementById("info").innerHTML=err;
        }
        else
        {
            ks.generateNewAddress(pwDerivedKey);
            var addresses = ks.getAddresses();

            var nets = document.getElementById("network").value;
            var net = select_net(nets);
            var web3 = new Web3(new Web3.providers.HttpProvider(net));
            var html = "";
            var address = addresses[0];
            var private_key = ks.exportPrivateKey(address,pwDerivedKey);
            var balance = web3.eth.getBalance("0x"+address);
            html = html + "<li>";
            html = html + "<p><b>Address:</b>0x"+ address+ "</p>";
            html = html + "<p><b>Private Key:</b>0x" + private_key + "</p>";
            html = html + "<p><b>Balance:</b>"+web3.fromWei(balance,"ether")+"ether</p>";
            html = html + "</li>";
            document.getElementById("list").innerHTML = html;
}
});
});
}
function send_ether()
{
	var	seed = document.getElementById("seed").value;

	if(!lightwallet.keystore.isSeedValid(seed))
	{
		document.getElementById("info").innerHTML = "Please enter a valid seed";
		return;
	}

	var password = Math.random().toString();
        var hdPath = "m/44'/60'/0'/0";
	lightwallet.keystore.createVault({
		password: password,
	  	seedPhrase: seed,
                hdPathString: hdPath
	}, function (err, ks) {
	  	ks.keyFromPassword(password, function (err, pwDerivedKey) {
	    	if(err)
	    	{
	    		document.getElementById("info").innerHTML ="keyfrompassword:"+ err;
	    	}
	    	else
	    	{
	    		ks.generateNewAddress(pwDerivedKey);

	    		ks.passwordProvider = function (callback) {
			      	callback(null, password);
			    };

                            var nets = document.getElementById("network").value;
                            var net = select_net(nets);
			    var provider = new HookedWeb3Provider({
  					host: net,
  					transaction_signer: ks
				});

			    var web3 = new Web3(provider);

			    var from = document.getElementById("from_address").value;
			    var to = document.getElementById("to_address").value;
			    var gasprice = web3.toWei(document.getElementById("gas_price").value, "Gwei");
                var data = document.getElementById("data").value;
                var value = web3.toWei(document.getElementById("ether").value, "ether");
                var gas = document.getElementById("gas").value;
				var t_value = document.getElementById("amount").value;
				if (data!="")
                {
                      var amount = t_value.toString(16);
                      var len =64-amount.length;
					  var o="0";
					  o=o.repeat(len);
                      data="0xa9059cbb"+"000000000000000000000000"+data.slice(2)+o+amount;
	    		      document.getElementById("info").innerHTML ="data:"+ data;
                }
				if(gas=="")
						gas=21000;
			    web3.eth.sendTransaction({
			    	from: from,
			    	to: to,
			    	value: value,
                    gas: gas,
                    gasPrice: gasprice,
                    data: data
			    }, function(error, result){
			    	if(error)
			    	{
			    		document.getElementById("info").innerHTML ="sendtransaction:"+ error;
			    	}
			    	else
			    	{
			    		document.getElementById("info").innerHTML = "Txn hash: " + result;
			    	}
			    })
	    	}
	  	});
	});
}
function send_ether()
{

}
