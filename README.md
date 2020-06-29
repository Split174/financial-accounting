# financial-accounting
## Orange-studio
 - Назаров Всеволод
 - Попов Сергей
 - Курдюков Павел
## Линки на документацию:
 - [ТЗ](https://drive.google.com/file/d/12CkJDKr_Eflnk-zWaBSYH7Zd6-0FX5tk/view)
 - [Спецификация API](https://docs.google.com/document/d/1xg3NZ3RpuQl9IU6-0tuarpGGm2oLYfA8KXk4T5s1i-E/edit)
 - [Концептуальная модель](https://drive.google.com/file/d/1pAKVBMlXmoawyK5nfflwhfDzvdU9OdWp/view) 
 - [Логическая модель](https://drive.google.com/file/d/1cGC8YWOpqPNwhYeId6UYIvbG5T2vCuWk/view) 
 - [Физическая модель](https://dbdesign.online/model/pSDA2teLCIHQ)

 ## Установка:
 <code>
 git clone https://github.com/Split174/financial-accounting accountFinance
 pip3 install poetry
 cd accountFinance/financial-accounting
 poetry install
 </code>


 ## Запуск:
 - Linux:
    <code>bash start.sh</code>
 - Windows: 
    <code>
      set PYTHONPATH=./src
      set FLASK_APP=app:create_app
      set FLASK_ENV=development
      flask run
    </code>

  
 
