import sqlite3
import config
import csv
import pathlib
import json
import io
import matplotlib.pyplot as plt
from utils import read_mit_fig, read_mit_data
import os
from PIL import Image


class Database:
    def __init__(self, csv_file, database_file = "output.json", start_row=0):
        self.read_csv = csv_file
        self.rows = list((line for line in csv.DictReader(open(self.read_csv, newline=''))))
        self.row_counter = self.get_index() + 1
        self.db = pathlib.Path(database_file)
        try:
            if not self.db.exists():
                with pathlib.Path.open(self.db, 'w') as inf:
                    inf.write(json.dumps([]))

        except:
            pass

    def get_index(self):
        row_counter = 0
        with open('last_sent_line.json') as inf:
            data = json.load(inf)
            row_counter = data['line']
        return row_counter

    def index_update(self):
        with open('last_sent_line.json', 'w+') as inf:
            data = json.dumps({'line': self.row_counter})
            inf.write(data)

    def getImg(self, path):
        buf = io.BytesIO()
        fig = read_mit_fig(path)

        fig.savefig(buf, format='jpg', dpi=120)
        buf.seek(0)
        # pil_img = Image.open(buf)
        # buf.close()
        plt.close(fig)
        return buf

    def getNext(self):
        counter = self.row_counter
        report = self.rows[self.row_counter]['report']
        path = os.path.join(config.MIT_DB, self.rows[self.row_counter]['patient_id'], f'{self.rows[self.row_counter]["date_of_test"]}_{self.rows[self.row_counter]["test_id"]}')
        img = self.getImg(path)
        data = read_mit_data(path)

        return self.row_counter, self.rows[self.row_counter]['report'], img, data

    def getTotal(self):
        return len(self.rows)

    def __read(self) -> dict:
        try:
            with pathlib.Path.open(self.db, 'r') as output:
                data = json.load(output)
        except json.JSONDecodeError as err:
            raise
        except FileNotFoundError as err:
            raise
        except:
            import traceback
            s = traceback.format_exc()
        return data

    def __write(self, json_data) -> bool:
        """ Write file """
        try:
            with pathlib.Path.open(self.db, 'w') as output:
                json_ = json.dumps(json_data, indent=4)
                output.write(json_)
        except json.JSONDecodeError as err:
            raise
        except FileNotFoundError as err:
            raise
        except:
            import traceback
            s = traceback.format_exc()

        return True


    def send(self, table_idx, data: dict):
        print('Запись в базу', table_idx, data)
        line = self.rows[self.row_counter]
        line['norma'] = data['norma']
        line['rhythm'] = data['rhythm']
        line['blocks'] = data['blocks']
        line['hypertrophy'] = data['hypertrophy']
        if len(data['skip']) or not (data['rhythm'] or data['blocks'] or data['hypertrophy']):
            line['isBad'] = True
        else:
            line['isBad'] = False

        json_data = self.__read()
        json_data.append(line)
        if self.__write(json_data):
            self.index_update()


        self.row_counter += 1