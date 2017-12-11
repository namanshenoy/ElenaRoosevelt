from flask import Flask
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    jason = [
      {
        "lat": 42.374641,
        "lon": -72.527458
      },
      {
        "lat": 42.372662,
        "lon": -72.526769
      },
      {
        "lat": 42.372604,
        "lon": -72.526521
      },
      {
        "lat": 42.372459,
        "lon": -72.526683
      },
      {
        "lat": 42.370289,
        "lon": -72.525776
      },
      {
        "lat": 42.37101,
        "lon": -72.524327
      },
      {
        "lat": 42.3716005,
        "lon": -72.5231617
      },
      {
        "lat": 42.372123,
        "lon": -72.52211
      },
      {
        "lat": 42.372461,
        "lon": -72.521438
      },
      {
        "lat": 42.372617,
        "lon": -72.521136
      },
      {
        "lat": 42.373212,
        "lon": -72.519809
      },
      {
        "lat": 42.373214,
        "lon": -72.518882
      },
      {
        "lat": 42.374794,
        "lon": -72.518929
      },
      {
        "lat": 42.375477,
        "lon": -72.5189807
      },
      {
        "lat": 42.375706,
        "lon": -72.518998
      },
      {
        "lat": 42.3757199,
        "lon": -72.5189135
      },
      {
        "lat": 42.3757604,
        "lon": -72.5183096
      },
      {
        "lat": 42.3762057,
        "lon": -72.5184709
      },
      {
        "lat": 42.3767907,
        "lon": -72.5188602
      },
      {
        "lat": 42.3767951,
        "lon": -72.5187387
      },
      {
        "lat": 42.377578,
        "lon": -72.518659
      },
      {
        "lat": 42.3775719,
        "lon": -72.5190816
      },
      {
        "lat": 42.37756,
        "lon": -72.5199108
      },
      {
        "lat": 42.3780544,
        "lon": -72.5199164
      },
      {
        "lat": 42.378757,
        "lon": -72.51992
      },
      {
        "lat": 42.379239,
        "lon": -72.519771
      },
      {
        "lat": 42.380001,
        "lon": -72.51948
      },
      {
        "lat": 42.3799486,
        "lon": -72.5187703
      },
      {
        "lat": 42.3803827,
        "lon": -72.5186457
      },
      {
        "lat": 42.3805973,
        "lon": -72.5191616
      },
      {
        "lat": 42.380615,
        "lon": -72.5193662
      },
      {
        "lat": 42.381221,
        "lon": -72.519293
      },
      {
        "lat": 42.381494,
        "lon": -72.519256
      },
      {
        "lat": 42.3818817,
        "lon": -72.5192151
      },
      {
        "lat": 42.383062,
        "lon": -72.518922
      },
      {
        "lat": 42.383787,
        "lon": -72.518439
      },
      {
        "lat": 42.3842435,
        "lon": -72.5181425
      },
      {
        "lat": 42.3844829,
        "lon": -72.5180024
      },
      {
        "lat": 42.38723,
        "lon": -72.517103
      },
      {
        "lat": 42.388314,
        "lon": -72.516937
      },
      {
        "lat": 42.3887088,
        "lon": -72.5168853
      },
      {
        "lat": 42.392618,
        "lon": -72.51643
      },
      {
        "lat": 42.392771,
        "lon": -72.518079
      },
      {
        "lat": 42.3930545,
        "lon": -72.5181798
      },
      {
        "lat": 42.3935529,
        "lon": -72.518292
      },
      {
        "lat": 42.3939407,
        "lon": -72.5180733
      },
      {
        "lat": 42.394219,
        "lon": -72.518047
      },
      {
        "lat": 42.3947097,
        "lon": -72.5180646
      },
      {
        "lat": 42.3958617,
        "lon": -72.5179441
      },
      {
        "lat": 42.3961777,
        "lon": -72.5177699
      },
      {
        "lat": 42.3969846,
        "lon": -72.5176866
      },
      {
        "lat": 42.3970494,
        "lon": -72.5179156
      },
      {
        "lat": 42.3971284,
        "lon": -72.5184958
      },
      {
        "lat": 42.39718,
        "lon": -72.519157
      },
      {
        "lat": 42.397279,
        "lon": -72.520115
      },
      {
        "lat": 42.397269,
        "lon": -72.5202307
      },
      {
        "lat": 42.3971928,
        "lon": -72.5211656
      },
      {
        "lat": 42.397786,
        "lon": -72.521305
      },
      {
        "lat": 42.398123,
        "lon": -72.522858
      },
      {
        "lat": 42.3982912,
        "lon": -72.5232199
      },
      {
        "lat": 42.3983424,
        "lon": -72.5232183
      },
      {
        "lat": 42.3981898,
        "lon": -72.5241882
      },
      {
        "lat": 42.3979835,
        "lon": -72.5248166
      },
      {
        "lat": 42.3977587,
        "lon": -72.5255423
      },
      {
        "lat": 42.3975911,
        "lon": -72.5263751
      },
      {
        "lat": 42.3976053,
        "lon": -72.5265775
      },
      {
        "lat": 42.3973943,
        "lon": -72.5274197
      },
      {
        "lat": 42.3972386,
        "lon": -72.527873
      },
      {
        "lat": 42.398044,
        "lon": -72.52807
      },
      {
        "lat": 42.398235,
        "lon": -72.528072
      },
      {
        "lat": 42.398368,
        "lon": -72.527578
      },
      {
        "lat": 42.3984314,
        "lon": -72.5274164
      },
      {
        "lat": 42.398876,
        "lon": -72.526714
      },
      {
        "lat": 42.3991108,
        "lon": -72.5260933
      },
      {
        "lat": 42.400578,
        "lon": -72.525103
      },
      {
        "lat": 42.400986,
        "lon": -72.523704
      },
      {
        "lat": 42.4011119,
        "lon": -72.5234499
      },
      {
        "lat": 42.4012582,
        "lon": -72.5230329
      },
      {
        "lat": 42.4014154,
        "lon": -72.5225979
      },
      {
        "lat": 42.4018418,
        "lon": -72.5211812
      },
      {
        "lat": 42.402017,
        "lon": -72.52092
      },
      {
        "lat": 42.402371,
        "lon": -72.520995
      },
      {
        "lat": 42.402442,
        "lon": -72.521001
      },
      {
        "lat": 42.4044548,
        "lon": -72.5219848
      },
      {
        "lat": 42.404671,
        "lon": -72.521262
      },
      {
        "lat": 42.405119,
        "lon": -72.519906
      },
      {
        "lat": 42.405126,
        "lon": -72.519882
      },
      {
        "lat": 42.405276,
        "lon": -72.518408
      },
      {
        "lat": 42.405593,
        "lon": -72.5147
      },
      {
        "lat": 42.406564,
        "lon": -72.51454
      },
      {
        "lat": 42.40798,
        "lon": -72.514311
      },
      {
        "lat": 42.408281,
        "lon": -72.514259
      },
      {
        "lat": 42.408608,
        "lon": -72.514198
      },
      {
        "lat": 42.40923,
        "lon": -72.514065
      },
      {
        "lat": 42.410688,
        "lon": -72.513701
      },
      {
        "lat": 42.4129141,
        "lon": -72.5131691
      },
      {
        "lat": 42.4131483,
        "lon": -72.5119323
      },
      {
        "lat": 42.4131082,
        "lon": -72.5089991
      },
      {
        "lat": 42.413813,
        "lon": -72.508497
      },
      {
        "lat": 42.413995,
        "lon": -72.508434
      },
      {
        "lat": 42.415637,
        "lon": -72.507865
      }
    ]

    return json.dumps(jason)

if __name__ == '__main__':
    app.run(debug=True)