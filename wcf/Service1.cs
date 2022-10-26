using System;
using System.Collections.Generic;

namespace wcf_training {
    // ПРИМЕЧАНИЕ. Команду "Переименовать" в меню "Рефакторинг" можно использовать для одновременного изменения имени класса "Service1" в коде и файле конфигурации.
    public class Service1 : IService1 {
        private readonly SQLiteConnector _connector = new SQLiteConnector("cars.db");
        private readonly string _insertTownSqlFormat = "INSERT INTO TOWNS(TOWN_NAME, DISTRICT_ID, TOWN_TYPE, POPULATION) VALUES('{0}',{1},'{2}',{3});";
        
        public void GetData(int region_id, string townName, string type, int population) {
            string insertTownSql = String.Format(_insertTownSqlFormat, townName, region_id, type, population);
            _connector.Execute(insertTownSql);
        }

        public CompositeType GetDataUsingDataContract(CompositeType composite) {
            if (composite == null) {
                throw new ArgumentNullException("composite");
            }
            if (composite.BoolValue) {
                composite.StringValue += "Suffix";
            }
            return composite;
        }
    }
}
