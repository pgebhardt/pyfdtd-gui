import QtQuick 1.1
import MatplotLib 1.0
import QtDesktop 0.1

// main window for pyfdtd-gui application
Window {
    // init window
    title: 'Pyfdtd GUI'
    width: 1000; height: 600

    // create menu
    MenuBar {
        id: menuBar

        // file menu
        Menu {
            id: fileMenu
            text: 'File'

            MenuItem {
                text: '&Open'
                shortcut: 'Ctrl+O'
            }
        }
    }

    // create root layout
    TabFrame {
        id: root
        anchors.fill: parent

        // simulation tab
        Tab {
            id: simTab
            title: 'Simulation'
            anchors.fill: parent

            // layout
            Grid {
                id: simLayout
                anchors.fill: parent
                columns: 2
                spacing: 2

                // plot
                Plot {
                    width: simTab.width / 2 - simLayout.spacing
                    height: simTab.height - startButton.height -
                        simLayout.spacing
                }

                // tree
                TableView {
                    id: tree
                    width: simTab.width / 2 - simLayout.spacing
                    height: simTab.height - startButton.height -
                        simLayout.spacing
                }

                Button {
                    id: startButton
                    text: 'Start Simulation'
                    width: plot.width
                }

                Button {
                    id: newLayerButton
                    text: 'New Layer'
                    width: tree.width
                }
            }
        }

        // evaluation tab
        Tab {
            id: evalTab
            title: 'Evaluation'

        }
    }
}
