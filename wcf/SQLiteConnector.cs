using System;
using System.Data.SQLite;
using System.Collections.Generic;

namespace wcf_training {
    class SQLiteConnector {
        private readonly SQLiteConnection _connection;

        public SQLiteConnector(String databasePath) {
            _connection = new SQLiteConnection($"Data Source={databasePath};Version=3;New=True;Compress=True;");
            _connection.Open();
        }

        public void Execute(String query) {
            SQLiteCommand cmd = _connection.CreateCommand();
            cmd.CommandText = query;
            cmd.ExecuteNonQuery();
        }

        public List<List<String>> ReadData(String query) {
            SQLiteCommand cmd = _connection.CreateCommand();
            cmd.CommandText = query;

            SQLiteDataReader reader = cmd.ExecuteReader();
            List<List<String>> queryResult = new List<List<String>>();
            while (reader.Read()) {
                List<String> row = new List<String>(reader.FieldCount);
                for (int i = 0; i < reader.FieldCount; i++) {
                    row.Add(reader.GetValue(i).ToString());
                }
                queryResult.Add(row);
            }

            return queryResult;
        }

        public void Close() {
            _connection.Close();
        }
    }
}
