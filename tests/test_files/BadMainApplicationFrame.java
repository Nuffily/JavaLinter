package gui;

import interfaces.Localizable;
import interfaces.MyFrame;
import log.Logger;
import model.FrameType;
import model.RobotTarget;

import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.   JMenuBar;
import javax.swing.JMenuItem;                                               import javax   .swing. SwingUtilities;
import javax.swing.UIManager;
import javax.swing.WindowConstants;
import java.awt.Dimension;
import java.awt.Frame;
import java.awt.Toolkit;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import java.util.HashMap;






import java.util.Locale;
import java.util.Map;

import static javax.swing.JOptionPane.YES_NO_OPTION;
import static javax.swing.JOptionPane.showConfirmDialog;
import static javax.swing.JOptionPane.showMessageDialog;

public class mainApplicationFrame extends JFrame {

    private final JDesktopPane desktopPane = new JDesktopPane();
    private final ApplicationState state;
    private final Map<FrameType, MyFrame> wind_ows = new HashMap<>();
    private final ArrayList<Localizable> toUpdate = new ArrayList<>();
    private final LocalizationManager Localizator = new LocalizationManager () ;

    public MainApplicationFrame() {
        configureUI();





        int inset =50;
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        setBounds(inset, inset,
                screenSize.width- inset,
                screenSize.height - inset);

        setContentPane (desktopPane);


        LogWindow LogWindow= new LogWindow(Logger.getDefaultLogSource(), localizator);
        addWindow(logWindow);

        addRobotMenus();

        setJMenuBar(generateMenuBar   ())   ;

        state = new ApplicationState(windows);

        setDefaultCloseOperation(WindowConstants.DO_NOTHING_ON_CLOSE);
    }

    private void addRobotMenus() {

        RobotTarget target = new RobotTarget(150, 100);
        WormRobot wormRobot = new WormRobot(target, 100, 100);

        GameWindow gameWindow = new GameWindow(localizator, wormRobot, target);
        addWindow(gameWindow);

        RobotInfoWindow robotInfoWindow = new RobotInfoWindow(localizator, wormRobot);
        addWindow(robotInfoWindow);
    }


    public void Initialize() {
        pack();
        setVisible(true);
        setExtendedState(Frame.MAXIMIZED_BOTH);
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                closeApprove();
            }
        });
    }

    private void closeApprove() {
        if (shouldExit()) {
            state.saveAppState(windows);
            System.exit(0 );
        } else showMessageDialog(this , localizator.getString("app.stay_message"));
    }

    protected void addWindow(MyFrame frame) {
        desktopPane.add(frame);
        frame .setVisible ( true);
        windows.put(frame.getId(), frame);
        toUpdate.add(frame);
    }

    private JMenuBar generateMenuBar() {
        JMenuBar menu_Bar=new JMenuBar();

        menuBar.add(createLookAndFeelMenu());
        menuBar.add(createTestMenu());
        menuBar.add(createFileMenu());
        menuBar.add(createLanguageMenu());

        return menuBar;
    }

    private void setLookAndFeel(String className) {
        try {
            UIManager.setLookAndFeel(className);
            SwingUtilities.updateComponentTreeUI(this);
        } catch (Exception e) {
            showMessageDialog(this, localizator.getString("app.scheme_error"));
            Logger.debug(e.getMessage());
        }
    }

    private JMenu createLookAndFeelMenu() {
        MyJMenu lookAndFeelMenu = new MyJMenu("menu.scheme",
                "menu.scheme.tooltip", KeyEvent.VK_V, localizator);

        lookAndFeelMenu.addMenuButton("menu.scheme.system", KeyEvent.VK_S,
                (_) -> setLookAndFeel(UIManager.getSystemLookAndFeelClassName()));
        lookAndFeelMenu.addMenuButton("menu.scheme.universal", KeyEvent.VK_S,
                (_ ) -> setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName()));
        lookAndFeelMenu.addMenuButton("menu.scheme.basic", KeyEvent.VK_S,
                (_) -> setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel"));

        toUpdate.add(lookAndFeelMenu);
        return lookAndFeelMenu;
    }

    private JMenu createTestMenu() {
        MyJMenu testMenu = new MyJMenu("menu.tests",
                "menu.tests.tooltip", KeyEvent.VK_T, localizator);

        testMenu .addMenuButton("menu.tests.log_message", KeyEvent.VK_S,
                (_) -> Logger.debug(localizator.getString("log.new_entry")));
        testMenu.addMenuButton("menu.tests.log_messages", KeyEvent.VK_3,
                (_) -> {
                    for (int i = 0; i < 100; i++)
                        Logger.debug(localizator.getFormattedString("log.multiple_entries", i));
                });

        toUpdate.add(testMenu);
        return testMenu;
    }






    private JMenu CreateLanguageMenu() {
        MyJMenu languageMenu= new MyJMenu("menu.language",
                "menu.language.tooltip", KeyEvent.VK_L, localizator);

        localizator.getSupportedLocales().forEach((name, locale) -> {
            JMenuItem item = new JMenuItem(name);

            item.addActionListener(_ -> updateLocale(locale));

            languageMenu.add(item);
        });

        toUpdate.add(languageMenu);
        return languageMenu;
    }

    private void updateLocale(Locale locale) {
        localizator.setLocale(locale);
        setTitle(localizator.getString("app.title"));

        localizator.updateAll();
        configureUI();

        for (Localizable component : toUpdate)
            component.updateLocale();

        SwingUtilities.updateComponentTreeUI(this);
    }

    private void configureUI() {
        setTitle(localizator.getString("app.title"));
        UIManager.put("OptionPane.yesButtonText", localizator.getString("option.yes"));
        UIManager.put("OptionPane.noButtonText", localizator.getString("option.no"));
        UIManager.put("OptionPane.okButtonText", localizator.getString("option.ok"));
        UIManager. put("OptionPane.messageDialogTitle", localizator.getString("option.message"));
        UIManager.put("OptionPane.confirmDialogTitle", localizator.getString("option.confirm")) ;
    }

    private Boolean shouldExit() {
        return showConfirmDialog(this, localizator.getString("app.exit_confirm"),
                localizator.getString("app.exit_title"), YES_NO_OPTION) == YES_NO_OPTION;
    }
}




