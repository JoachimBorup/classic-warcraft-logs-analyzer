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

Here is an examples of the output of the `analyze` command on fight [6](
https://classic.warcraftlogs.com/reports/TJwWr16NBgZdtyRY#fight=6) and [7](
https://classic.warcraftlogs.com/reports/TJwWr16NBgZdtyRY#fight=7) of a report on Lady Deathwhisper:

```bash
$ python main.py analyze TJwWr16NBgZdtyRY --name "Lady Deathwhisper" --fights 6 7

Retrieved report TJwWr16NBgZdtyRY after 3.64 seconds!

Report consists of 2 fights:
Wiped on Lady Deathwhisper (Heroic) at 67.06%:
- All deaths:
  - Bonkdy died to Melee at 1:45
  - Heiseen died to Melee at 2:42
  - Zularjar died to Seal of Command at 3:28
  - Näf died to Melee at 3:39
  - Ezali died to Vengeful Blast at 4:20
  - Ezali died to Vengeful Blast at 4:41
  - Jaóel died to Vengeful Blast at 4:42
  - Bigmojoe died to Vengeful Blast at 4:42
  - Ulverr died to Vengeful Blast at 4:42
  - Chadshimi died to Vengeful Blast at 4:42
  - Frozenclaws died to Vengeful Blast at 4:59
  - Jaóel died to Vengeful Blast at 4:59
  - Heiseen died to Vengeful Blast at 4:59
  - Chadshimi died to Vengeful Blast at 4:59
  - Bonkdy died to Vengeful Blast at 4:59
  - Korrashiba died to Vengeful Blast at 4:59
  - Altaltetude died to Frostbolt Volley at 5:01
  - Zularjar died to Vengeful Blast at 5:06
  - Druxus died to Vengeful Blast at 5:06
  - Tjals died to Vengeful Blast at 5:06
  - Lammaz died to Vengeful Blast at 5:06
  - Myrilia died to Melee at 5:11
  - Zeliik died to Death and Decay at 5:12
  - Ayyitsspring died to Death and Decay at 5:13
  - Daishax died to Deathchill Bolt at 5:15
  - Wackjoe died to Frostbolt at 5:15
  - Yungchaddy died to Melee at 5:17
  - Crackberry died to Deathchill Bolt at 5:18
- Most common deaths:
  - Vengeful Blast: 16
  - Melee: 5
  - Death and Decay: 2
Wiped on Lady Deathwhisper (Heroic) at 40.07%:
- All deaths:
  - Druxus died to Dark Martyrdom at 1:06
  - Druxus died to Melee at 3:29
  - Altaltetude died to Frostbolt Volley at 4:13
  - Ulverr died to Frostbolt Volley at 4:14
  - Korrashiba died to Vengeful Blast at 4:36
  - Chadshimi died to Vengeful Blast at 5:04
  - Druxus died to Vengeful Blast at 5:16
  - Tjals died to Vengeful Blast at 5:16
  - Altaltetude died to Vengeful Blast at 5:46
  - Wackjoe died to Frostbolt at 6:13
  - Skadadin died to Vengeful Blast at 6:23
  - Zularjar died to Melee at 6:38
  - Bonkdy died to Vengeful Blast at 6:40
  - Lammaz died to Vengeful Blast at 6:40
  - Daishax died to Frostbolt Volley at 6:40
  - Yungchaddy died to Frostbolt Volley at 6:40
  - Jaóel died to Vengeful Blast at 6:48
  - Crackberry died to Melee at 6:49
  - Zeliik died to Hammer of Wrath at 6:59
  - Näf died to Frostbolt Volley at 7:00
  - Myrilia died to Frostbolt Volley at 7:01
  - Croyman died to Frostbolt Volley at 7:01
- Most common deaths:
  - Vengeful Blast: 9
  - Frostbolt Volley: 7
  - Melee: 3
```
