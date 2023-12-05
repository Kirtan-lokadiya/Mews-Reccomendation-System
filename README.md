# News-Reccomendation-System

I have made two model for reccomendation
1) First one does reccomendation based on the user's interaction history
2) The second one does reccomendaton based on the content user is reading

The full wokflow of the system would be:

First the user will be shown reccomndations based on his history, ----> The first model
which would be seperated by categories.
whichever news user will click on , this data will be saved to further train the user history model
after reading the news, then user will get further reccomendations based on the content of the news ----> The Second model

We will have to call the prediction API accordingly,
the prediction APIs are present in :
src/News_Reccomendation_System/pipeline/step4_prediction.py


# how to run

```bash
git clone (this repo)
```
```bash
docker build -t app .
```
```bash
docker run -d -p 80:5000 app```

Then go to localhost:80/

## voila it works 