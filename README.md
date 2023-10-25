# Classic Warcraft Logs Analyzer

## Description

This is a tool to analyze the logs from Classic WoW from [Warcraft Logs](https://classic.warcraftlogs.com/).
It is written in Python and uses the [Warcraft Logs API](https://www.warcraftlogs.com/api/docs) to fetch the data.

## Pre-requisites

### Python packages

Run the following command to install the required Python packages:

```bash
pip install -r requirements.txt
```

### Warcraft Logs access token

Warcraft Logs uses OAuth 2.0 for API authentication. OAuth allows clients to use an access token to authenticate API
requests. To get an access token, you need to create an API client on the Warcraft Logs website. You can do this by
going to the [client management page](https://www.warcraftlogs.com/api/clients/) and clicking the "Create Client"
button. You will need to do the following:

- Enter a name for your client. This can be anything you want.
- Enter a redirect URL for your client. You should set this to `https://localhost:5000/callback`.
- Don't select the "Public" option, as you can store your client secret securely in an environment variable.

Once you have created your client, you will be shown your client ID and client secret. You will need to store these in
environment variables called `WCL_CLIENT_ID` and `WCL_CLIENT_SECRET` respectively. You can do this by adding them to a
`.env` file in the root directory of the project, or by running the following commands:

```bash
export WCL_CLIENT_ID=<your client ID>
export WCL_CLIENT_SECRET=<your client secret>
```

To get your access token, either follow the instructions in the [Warcraft Logs API documentation](
https://www.warcraftlogs.com/api/docs#client-credentials-flow) or run the following command:

```bash
python main.py token
```

This will open a browser window where you can log in to Warcraft Logs and authorize your client. Once you have done
this, you will be redirected to a new page. Copy the URL of this page and paste it into the terminal. The access token
will then be printed to the terminal. Store this in an environment variable called `WCL_ACCESS_TOKEN` by adding it to a
`.env` file in the root directory of the project, or by running the following command:

```bash
export WCL_ACCESS_TOKEN=<your access token>
```

## Usage

### Analyzing a report

To analyze a report, run the following command using the report ID from the URL of the report page on Warcraft Logs:

```bash
python main.py analyze <report ID>
```

To restrict the analysis to a specific boss and/or fights, use the optional `--name` (alternatively, `--encounter`) and `--fights` flags:

```bash
python main.py analyze <report ID> --name <encounter name> --fights <fight IDs>
```

#### Example

Here are some examples of the output of the `analyze` command:

```bash
$ python main.py analyze TJwWr16NBgZdtyRY --name "Lady Deathwhisper"

Retrieving report TJwWr16NBgZdtyRY from Warcraft Logs...
Retrieved report TJwWr16NBgZdtyRY!

Report consists of 5 fights:
- Wiped on Lady Deathwhisper (Heroic) at 77.59%
- Wiped on Lady Deathwhisper (Heroic) at 67.06%
- Wiped on Lady Deathwhisper (Heroic) at 40.07%
- Wiped on Lady Deathwhisper (Heroic) at 99.98%
- Killed Lady Deathwhisper (Normal)
```

```bash
$ python main.py analyze TJwWr16NBgZdtyRY --encounter 848 --type wipes

Retrieving report TJwWr16NBgZdtyRY from Warcraft Logs...
Retrieved report TJwWr16NBgZdtyRY!

Report consists of 2 fights:
- Wiped on Deathbringer Saurfang (Heroic) at 55.28%
- Wiped on Deathbringer Saurfang (Heroic) at 30.16%
```
