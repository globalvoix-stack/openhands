const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('thinksoft-hello-world.helloWorld', function () {
        vscode.window.showInformationMessage('Hello from Thinksoft!');
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}
