var login_button = 'button[name="Login"]';
var login_form = 'form[action="/Login"]';

var register_button = 'button[name="Register"]';
var register_form = 'form[action="/Register"]';

var submit_button = 'button[name="submit"]';
var registration_form = 'form[action="/Registration"]'

var spawn = require("child_process").spawn
var webpath = "/Users/neko1990/Work/ICM2015/"


var base_url = "http://localhost:8000";
casper.test.begin( 'casper tests for CUMT application', 8,function suite(test){
  casper.start(base_url, function(){
    test.assertTitleMatch(/International/, "Home page title expected");
    test.assertExists(login_button, "Register button is found");
    test.assertExists(register_button, "Login button is found");
  });
  casper.thenClick(register_button,function(){
    test.assertUrlMatch(/Register/, "Now at register page");
    test.assertExists(register_form);
  });
  casper.then(function (){
    this.fill(register_form,{
      'email':'user3@gmail.com',
      'password':'123456789',
      're_password':'123456789'
    },true);
  });
  casper.then(function(){
    test.assertUrlMatch(/SendApply/, "SendApply title expected");
  });
  casper.then(function(){
    phantom.clearCookies();
  });
  casper.thenOpen(base_url,function(){
    test.assertUrlMatch(/RegistrationGate/, "We cleared cookies, back to root");
  });
  casper.thenClick(login_button,function(){
    test.assertUrlMatch(/Login/, "Now at login page");
  });
  casper.then(function(){
    this.fill(login_form,{
      'email':'user3@gmail.com',
      'password':'123456789',
    },true);
  });
  casper.then(function(){
    test.assertUrlMatch(/SendApply/,"SendApply title expected");
  });
  casper.thenClick(submit_button,function(){
    test.assertUrlMatch(/Registration/,"Registration Url expected");
  });
  // casper.then(function(){
  //   this.click('input[name="gender"][value="Male"]');
  //   this.fillSelectors(registration_form, {
  //     'select[name*="college"]' :  "2",
  //   }, false);
  //   this.fill(registration_form,{
  //     'telephone':'18994900589',
  //     'num':'ZS13170005',
  //     'name':'cd',
  //   },true);
  // });
  // casper.then(function(){
  //   test.assertTextExists('Thank you form your Application!',"Thank you text expected");
  // });
  casper.run(function(){
    test.done();
  });
});

casper.test.setUp(function(){
  casper.echo('start server ...');
  var child = spawn("ls",["python",""])
});

casper.test.tearDown(function(){
  casper.echo('we done.');
});
