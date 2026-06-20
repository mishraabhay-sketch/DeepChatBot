def get_theme(theme_name):

    if theme_name == "Light":

        return """
        QWidget{
            background-color:white;
            color:black;
        }

        QPushButton{
            padding:8px;
        }

        QLineEdit, QTextEdit, QListWidget, QTableWidget{
            background:white;
            color:black;
        }
        """

    elif theme_name == "Cyber Blue":

        return """
        QWidget{
            background-color:#001122;
            color:#00ffff;
        }

        QPushButton{
            border:2px solid #00ffff;
            padding:8px;
        }
        """

    return """
    QWidget{
        background-color:#0f0f0f;
        color:white;
    }

    QPushButton{
        padding:8px;
    }
    """