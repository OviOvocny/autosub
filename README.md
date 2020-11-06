# autosub
Machine translation for ASS subtitles via MS Translator on Azure

----

This python script uses the [Microsoft Translator API](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-reference) (part of Azure Cognitive Services) to translate dialogue lines in ASS (Advanced Substation Alpha) subtitle files, from and to any of the supported languages. Some formatting tags and forced newlines may be sacrificed in the process.

## Usage
Before using the script, you need to grab a key for the Translator service. You'll need an Azure account and set up the Translator service, then get one of the keys provided. __The service allows translating some 2 million character per month for free.__ Should be more than enough for personal use of this script.

### Prerequisites
- Python 3.6 or newer
- `requests` python module, ex. installed via __pip__
- Translator API key

For ease of use, it is recommended to set the API key as environment variable __TRANSLATOR_KEY__ read by the script. Alternatively, you can provide it on each run as the `--key` argument.

### Using autosub from command line
The general CLI pattern is \
`autosub [-h] -l LANGUAGES [-s] [-v] [--key KEY] input [output]`\
Use `-h` to get help.

Required arguments:
- __Input__ and __output__ are paths to your files. Point input to the source .ass file and provide a path to write the output. Output is stdout by default.
- __-l__ or __--languages__ selects source and target language to configure the translator. Provided as `source:target` using laguage codes (ex. `en:de`) that can also be [listed via the Translator API](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-languages).

Optional arguments:
- __-s__ or __--stream__ is a flag. Also, you probably shouln't use it. It tells the script to translate line by line instead of buffering more lines and sending them all at once. Maybe it's less memory intensive, maybe it's useless, but it's definitely slow.
- __-v__ or __--verbose__ is a flag. This enables printing status messages __onto stdout__ reporting what's happening. Obviously, when file output is stdout, this doesn't do anything. You don't want statuses in your output.
- __--key__ lets you provide the API key as an argument instead of setting it in environment.

## Is this good?
No, of course not. Even if it doesn't screw up formatting or accidentaly skip lines, it's still just machine translation. Have fun.

## Why did you...
- ...use the Microsoft translator? Because I found it maybe does a better job here. Also, getting the API to work wasn't a nightmare.
- ...make this? Because I'm a lazy retired fansubber. This is surprisingly useful for translating. It does a bulk of the work for you, then you just make it make sense.

## Contributing
If you can make sense of the code, feel free to make any improvements, fixes, complete rewrites, whatever. I'll be here.