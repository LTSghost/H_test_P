from flask import Flask, render_template, jsonify, make_response, request
from pathlib import Path
import os
import requests
import datetime



# --- if ./static/test.txt not exist, then touch test.txt file

# fle = Path('./static/test.txt')   
# fle.touch(exist_ok=True)
# f = open(fle)



ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


# check allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def index():
    
    return render_template('index.html')


# ?orderBy={orderBy}&orderByDirection={orderByDirection}&filterByName={filterByName}
# ?orderBy=1&orderByDirection=dd&filterByName=LTS

@app.route('/file/<path:LSFP>',methods=['GET','POST','DELETE','PUT','PATCH'])
def file(LSFP):

    # filePath = f'./{root}/{usr}/test.txt'
    # if not os.path.exists(filePath):
    #     os.makedirs(filePath)
    #     os.

    # print('arg')


    # GET
    if request.method == "GET":

        # print(os.path.isfile(f'static/{LSFP}'))

        if os.path.isfile(f'static/{LSFP}'):

            local_file = LSFP.split('/')[-1]

            LFold_list = LSFP.split('/')[:-1]

            local_folder_path = '/'.join(str(i) for i in LFold_list)

            local_folder_path = f'static/{local_folder_path}'

            # mkdir /root/usr...etc...
            # if not os.path.exists(local_folder_path):
            #     os.makedirs(local_folder_path)

            # touch file
            fle = Path(f'{local_folder_path}/{local_file}')
            # fle.touch(exist_ok=True)
            # f = open(fle, "rb")

            file_size = os.path.getsize(fle)
            print(file_size)
            file_name = os.path.basename(fle)
            print(file_name)
            file_modify = os.path.getmtime(fle)
            file_modify = float(format(file_modify,'.2f'))
            file_modify = datetime.datetime.fromtimestamp(file_modify)
            print(file_modify)
            file_info = [file_size,file_name,file_modify]

            f = open(fle, "rb")


            # ?orderBy=[lastModified, size, fileName]&orderByDirection=[Descending , Ascending]&filterByName=test.txt

            if request.args:
                args = request.args

                print(args)
                if len(args) != 3:
                    return 'Not found', 404

                for k,v in args.items():
                    if k not in ['orderBy','orderByDirection','filterByName']:
                        return 'Not found', 404

                    print(k,v)


                serialized = ','.join(f'{k} : {v} ' for k,v in args.items())

                print(serialized)

                arg_list = [[k,v] for k,v in args.items()]

                return render_template('file.html',serialized=serialized,args=args, arg_list=arg_list,file_info=file_info,f=f)
            else:
                return 'Not Found', 404

        # mkdir /root/usr...etc...
        # if not os.path.exists(f'static/{LSFP}'):
        #     os.makedirs(f'static/{LSFP}')

        # f = jsonify({'isDirectory':os.path.isdir(f"static/{LSFP}"),'files':os.listdir(f"static/{LSFP}")})

        def file_modified(name):
            file_modify = os.path.getmtime(f'static/{LSFP}/{name}')
            file_modify = float(format(file_modify,'.2f'))
            file_modify = datetime.datetime.fromtimestamp(file_modify)
            # print(file_modify)
            return str(file_modify)


        tmp_list = []

        for i in os.listdir(f"static/{LSFP}"):
            tmp_list.append({
            "fileName":i,
            "size": os.path.getsize(f'static/{LSFP}/{i}'),
            "lastModified": file_modified(i)
        })

        # print(tmp_list)
        
        f = jsonify({'isDirectory':os.path.isdir(f"static/{LSFP}"),'files':tmp_list})

        # ?orderBy=[lastModified, size, fileName]&orderByDirection=[Descending , Ascending]&filterByName=test.txt

        if request.args:
            args = request.args

            print(args)
            if len(args) != 3:
                return 'Not found', 404

            for k,v in args.items():
                if k not in ['orderBy','orderByDirection','filterByName']:
                    return 'Not found', 404

                print(k,v)

            serialized = ','.join(f'{k} : {v} ' for k,v in args.items())

            print(serialized)

            arg_list = [[k,v] for k,v in args.items()]

            return make_response(f, 200)
        else:
            return 'Not Found', 404



    # POST
    if request.method == "POST":

        UPLOAD_FOLDER = f'static/{LSFP}'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


        file = request.files['file']
        # print(file)
        filename = file.filename
        # print(filename)
        # print(os.path.basename(f'{UPLOAD_FOLDER}/{filename}'))
        if os.path.exists(f'{UPLOAD_FOLDER}/{filename}'):
            return 'This file is existed',201
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # mkdir /root/usr...etc...
        # if not os.path.exists(f'static/{LSFP}'):
        #     os.makedirs(f'static/{LSFP}')

        return 'UPLOAD SUCCESSED', 200

    
     
    # PATCH
    # if request.method == "PATCH":
        
    
    # DELETE
    # if request.method == "DELETE":



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



if __name__ == "__main__":
    app.run(debug=True,port=5005)