#!/usr/bin/env python
# coding: utf-8

import random

import numpy
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from tqdm import tqdm

from model import Apk


class RiskInDroid(object):

    # Official Android permissions list (138 permissions):
    # http://developer.android.com/reference/android/Manifest.permission.html
    # noinspection SpellCheckingInspection
    ANDROID_PERMISSIONS = (
        'android.permission.ACCESS_CHECKIN_PROPERTIES',
        'android.permission.ACCESS_COARSE_LOCATION',
        'android.permission.ACCESS_FINE_LOCATION',
        'android.permission.ACCESS_LOCATION_EXTRA_COMMANDS',
        'android.permission.ACCESS_NETWORK_STATE',
        'android.permission.ACCESS_NOTIFICATION_POLICY',
        'android.permission.ACCESS_WIFI_STATE',
        'android.permission.ACCOUNT_MANAGER',
        'com.android.voicemail.permission.ADD_VOICEMAIL',
        'android.permission.BATTERY_STATS',
        'android.permission.BIND_ACCESSIBILITY_SERVICE',
        'android.permission.BIND_APPWIDGET',
        'android.permission.BIND_CARRIER_MESSAGING_SERVICE',
        'android.permission.BIND_CARRIER_SERVICES',
        'android.permission.BIND_CHOOSER_TARGET_SERVICE',
        'android.permission.BIND_CONDITION_PROVIDER_SERVICE',
        'android.permission.BIND_DEVICE_ADMIN',
        'android.permission.BIND_DREAM_SERVICE',
        'android.permission.BIND_INCALL_SERVICE',
        'android.permission.BIND_INPUT_METHOD',
        'android.permission.BIND_MIDI_DEVICE_SERVICE',
        'android.permission.BIND_NFC_SERVICE',
        'android.permission.BIND_NOTIFICATION_LISTENER_SERVICE',
        'android.permission.BIND_PRINT_SERVICE',
        'android.permission.BIND_QUICK_SETTINGS_TILE',
        'android.permission.BIND_REMOTEVIEWS',
        'android.permission.BIND_SCREENING_SERVICE',
        'android.permission.BIND_TELECOM_CONNECTION_SERVICE',
        'android.permission.BIND_TEXT_SERVICE',
        'android.permission.BIND_TV_INPUT',
        'android.permission.BIND_VOICE_INTERACTION',
        'android.permission.BIND_VPN_SERVICE',
        'android.permission.BIND_VR_LISTENER_SERVICE',
        'android.permission.BIND_WALLPAPER',
        'android.permission.BLUETOOTH',
        'android.permission.BLUETOOTH_ADMIN',
        'android.permission.BLUETOOTH_PRIVILEGED',
        'android.permission.BODY_SENSORS',
        'android.permission.BROADCAST_PACKAGE_REMOVED',
        'android.permission.BROADCAST_SMS',
        'android.permission.BROADCAST_STICKY',
        'android.permission.BROADCAST_WAP_PUSH',
        'android.permission.CALL_PHONE',
        'android.permission.CALL_PRIVILEGED',
        'android.permission.CAMERA',
        'android.permission.CAPTURE_AUDIO_OUTPUT',
        'android.permission.CAPTURE_SECURE_VIDEO_OUTPUT',
        'android.permission.CAPTURE_VIDEO_OUTPUT',
        'android.permission.CHANGE_COMPONENT_ENABLED_STATE',
        'android.permission.CHANGE_CONFIGURATION',
        'android.permission.CHANGE_NETWORK_STATE',
        'android.permission.CHANGE_WIFI_MULTICAST_STATE',
        'android.permission.CHANGE_WIFI_STATE',
        'android.permission.CLEAR_APP_CACHE',
        'android.permission.CONTROL_LOCATION_UPDATES',
        'android.permission.DELETE_CACHE_FILES',
        'android.permission.DELETE_PACKAGES',
        'android.permission.DIAGNOSTIC',
        'android.permission.DISABLE_KEYGUARD',
        'android.permission.DUMP',
        'android.permission.EXPAND_STATUS_BAR',
        'android.permission.FACTORY_TEST',
        'android.permission.GET_ACCOUNTS',
        'android.permission.GET_ACCOUNTS_PRIVILEGED',
        'android.permission.GET_PACKAGE_SIZE',
        'android.permission.GET_TASKS',
        'android.permission.GLOBAL_SEARCH',
        'android.permission.INSTALL_LOCATION_PROVIDER',
        'android.permission.INSTALL_PACKAGES',
        'com.android.launcher.permission.INSTALL_SHORTCUT',
        'android.permission.INTERNET',
        'android.permission.KILL_BACKGROUND_PROCESSES',
        'android.permission.LOCATION_HARDWARE',
        'android.permission.MANAGE_DOCUMENTS',
        'android.permission.MASTER_CLEAR',
        'android.permission.MEDIA_CONTENT_CONTROL',
        'android.permission.MODIFY_AUDIO_SETTINGS',
        'android.permission.MODIFY_PHONE_STATE',
        'android.permission.MOUNT_FORMAT_FILESYSTEMS',
        'android.permission.MOUNT_UNMOUNT_FILESYSTEMS',
        'android.permission.NFC',
        'android.permission.PACKAGE_USAGE_STATS',
        'android.permission.PERSISTENT_ACTIVITY',
        'android.permission.PROCESS_OUTGOING_CALLS',
        'android.permission.READ_CALENDAR',
        'android.permission.READ_CALL_LOG',
        'android.permission.READ_CONTACTS',
        'android.permission.READ_EXTERNAL_STORAGE',
        'android.permission.READ_FRAME_BUFFER',
        'android.permission.READ_INPUT_STATE',
        'android.permission.READ_LOGS',
        'android.permission.READ_PHONE_STATE',
        'android.permission.READ_SMS',
        'android.permission.READ_SYNC_SETTINGS',
        'android.permission.READ_SYNC_STATS',
        'com.android.voicemail.permission.READ_VOICEMAIL',
        'android.permission.REBOOT',
        'android.permission.RECEIVE_BOOT_COMPLETED',
        'android.permission.RECEIVE_MMS',
        'android.permission.RECEIVE_SMS',
        'android.permission.RECEIVE_WAP_PUSH',
        'android.permission.RECORD_AUDIO',
        'android.permission.REORDER_TASKS',
        'android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS',
        'android.permission.REQUEST_INSTALL_PACKAGES',
        'android.permission.RESTART_PACKAGES',
        'android.permission.SEND_RESPOND_VIA_MESSAGE',
        'android.permission.SEND_SMS',
        'com.android.alarm.permission.SET_ALARM',
        'android.permission.SET_ALWAYS_FINISH',
        'android.permission.SET_ANIMATION_SCALE',
        'android.permission.SET_DEBUG_APP',
        'android.permission.SET_PREFERRED_APPLICATIONS',
        'android.permission.SET_PROCESS_LIMIT',
        'android.permission.SET_TIME',
        'android.permission.SET_TIME_ZONE',
        'android.permission.SET_WALLPAPER',
        'android.permission.SET_WALLPAPER_HINTS',
        'android.permission.SIGNAL_PERSISTENT_PROCESSES',
        'android.permission.STATUS_BAR',
        'android.permission.SYSTEM_ALERT_WINDOW',
        'android.permission.TRANSMIT_IR',
        'com.android.launcher.permission.UNINSTALL_SHORTCUT',
        'android.permission.UPDATE_DEVICE_STATS',
        'android.permission.USE_FINGERPRINT',
        'android.permission.USE_SIP',
        'android.permission.VIBRATE',
        'android.permission.WAKE_LOCK',
        'android.permission.WRITE_APN_SETTINGS',
        'android.permission.WRITE_CALENDAR',
        'android.permission.WRITE_CALL_LOG',
        'android.permission.WRITE_CONTACTS',
        'android.permission.WRITE_EXTERNAL_STORAGE',
        'android.permission.WRITE_GSERVICES',
        'android.permission.WRITE_SECURE_SETTINGS',
        'android.permission.WRITE_SETTINGS',
        'android.permission.WRITE_SYNC_SETTINGS',
        'com.android.voicemail.permission.WRITE_VOICEMAIL')

    # Permissions can be only declared, declared and used etc.
    # 'allTypes' category combines all the other categories.
    PERMISSION_TYPES = ('declared',
                        'requiredAndUsed',
                        'requiredButNotUsed',
                        'notRequiredButUsed',
                        'allTypes')

    def __init__(self):

        # Random seed.
        self.seed = 42

        # List with the trained models.
        self.trained_models = []

        # List of classifiers used to compute the risk score.
        self.MODELS = (SVC(kernel='linear', probability=True, random_state=self.seed),
                       MultinomialNB(),
                       GradientBoostingClassifier(random_state=self.seed),
                       LogisticRegression(random_state=self.seed))

    def get_feature_vector(self, apk: Apk):

        _vector = {}

        # Create a new "row" for each category of permissions, where the columns
        # will be the permissions' names contained in ANDROID_PERMISSIONS.
        for permission_type in self.PERMISSION_TYPES:
            _vector[permission_type] = []

        _type_dict = {
            'declared': apk.declared_permissions,
            'requiredAndUsed': apk.required_and_used_permissions,
            'requiredButNotUsed': apk.required_but_not_used_permissions,
            'notRequiredButUsed': apk.not_required_but_used_permissions
        }

        for permission_type in self.PERMISSION_TYPES[:-1]:
            for permission in self.ANDROID_PERMISSIONS:

                # Insert 1 every time the app contains a certain permission, insert 0 otherwise.
                if permission in map(lambda x: x.name, _type_dict[permission_type]):
                    _vector[permission_type].append(1)
                    _vector['allTypes'].append(1)
                else:
                    _vector[permission_type].append(0)
                    _vector['allTypes'].append(0)

        return _vector

    def get_training_apks(self):

        # Get the entire list of apps belonging to the Malware Collection and to the
        # Google Play Store collection.
        _malware = Apk.query.filter_by(source='Malware Collection').all()
        _goodware = Apk.query.filter_by(source='Google Play').all()

        # There are many more apps in the Malware Collection than in the Google Play Store
        # collection, so for the training set we extract only a subset of apps belonging to
        # the Google Play Store collection, in order to have a balanced dataset with the
        # same number of benign and malign apps.

        # Set the seed for reproducibility purposes.
        random.seed(self.seed)

        random.shuffle(_goodware)

        _malware_set = _malware
        _goodware_set = _goodware[: len(_malware_set)]

        # Training apks.
        _apks = numpy.concatenate((_malware_set, _goodware_set))

        # Training targets.
        _targets = numpy.concatenate((numpy.full(len(_malware_set), _malware_set[0].type, dtype='S7'),
                                      numpy.full(len(_goodware_set), _goodware_set[0].type, dtype='S8')))

        return _apks, _targets

    def get_training_apks_3_sets(self):

        # Get the entire list of apps belonging to the Malware Collection and to the
        # Google Play Store collection.
        _malware = Apk.query.filter_by(source='Malware Collection').all()
        _goodware = Apk.query.filter_by(source='Google Play').all()

        # There are many more apps in the Malware Collection than in the Google Play Store
        # collection, so for the training set we extract only a subset of apps belonging to
        # the Google Play Store collection, in order to have a balanced dataset with the
        # same number of benign and malign apps. For testing purposes, we extract 3 different
        # random training sets.

        # Set the seed for reproducibility purposes.
        random.seed(self.seed)

        random.shuffle(_goodware)

        _malware_set = _malware
        _goodware_set_1 = _goodware[: len(_malware_set)]
        _goodware_set_2 = _goodware[len(_malware_set): 2 * len(_malware_set)]
        _goodware_set_3 = _goodware[2 * len(_malware_set): 3 * len(_malware_set)]

        # Training apk sets.
        _apks_1 = numpy.concatenate((_malware_set, _goodware_set_1))
        _apks_2 = numpy.concatenate((_malware_set, _goodware_set_2))
        _apks_3 = numpy.concatenate((_malware_set, _goodware_set_3))

        # Training targets (targets are the same for every training set).
        _targets = numpy.concatenate((numpy.full(len(_malware_set), _malware_set[0].type, dtype='S7'),
                                      numpy.full(len(_goodware_set_1), _goodware_set_1[0].type, dtype='S8')))

        return (_apks_1, _targets), (_apks_2, _targets), (_apks_3, _targets)

    def get_training_vectors(self):

        _apks, _targets = self.get_training_apks()

        _vectors = {}

        # Training vectors initialization.
        for permission_type in self.PERMISSION_TYPES:
            _vectors[permission_type] = []
        _vectors['target'] = []

        for apk in tqdm(_apks, dynamic_ncols=True, desc='Extracting feature vectors',
                        bar_format='{l_bar}{bar}|[{elapsed}<{remaining}]'):
            _vector = self.get_feature_vector(apk)

            for permission_type in self.PERMISSION_TYPES:
                _vectors[permission_type].append(_vector[permission_type])

            _vectors['target'].append(apk.type)

        return _vectors, _targets

    def get_training_vectors_3_sets(self):

        _sets = self.get_training_apks_3_sets()

        _vector_sets = []

        for (idx, s) in enumerate(_sets):
            _vectors = {}

            # Training vectors initialization.
            for permission_type in self.PERMISSION_TYPES:
                _vectors[permission_type] = []
            _vectors['target'] = []

            for apk in tqdm(s[0], dynamic_ncols=True, desc='Extracting feature vectors (set {0})'.format(idx + 1),
                            bar_format='{l_bar}{bar}|[{elapsed}<{remaining}]'):
                _vector = self.get_feature_vector(apk)

                for permission_type in self.PERMISSION_TYPES:
                    _vectors[permission_type].append(_vector[permission_type])

                _vectors['target'].append(apk.type)

            _vector_sets.append(_vectors)

        return ((v, v['target']) for v in _vector_sets)

    def train_classifiers(self):

        _vectors, _targets = self.get_training_vectors()

        self.trained_models = []

        # Train all the selected classifiers.
        for model in tqdm(self.MODELS, dynamic_ncols=True, desc='Training classifiers',
                          bar_format='{l_bar}{bar}|[{elapsed}<{remaining}]'):
            model.fit(_vectors['allTypes'], _targets)
            self.trained_models.append(model)

        return self.trained_models

    def calculate_risk(self, feature_vector: dict):

        # Get the desired category from the feature vector for the app under test.
        _test_app = feature_vector['allTypes']

        # If the classifiers are not already trained, train them.
        if not self.trained_models:
            self.train_classifiers()

        # Compute the probability for every classifier in the list, indicating the risk of test_app.
        _probas = [list(zip(model.classes_, model.predict_proba([_test_app])[0])) for model in self.trained_models]

        _mean_proba = numpy.array([])

        # Get the mean probability generated by the classifiers.
        for proba in _probas:

            # The risk score is given by the probability associated
            # with "malware" class output from the classifiers.
            if proba[0][0] == 'malware':
                _score = proba[0]
            else:
                _score = proba[1]

            _mean_proba = numpy.append(_mean_proba, _score[1])

        # Rescale the risk value in order to avoid probabilities too close to 0 and 1.
        _risk_value = 100 * _mean_proba.mean()
        # noinspection PyUnresolvedReferences
        _rescaled_risk = (50 / numpy.log(101)) * (numpy.log(_risk_value + 1) - numpy.log(101 - _risk_value)) + 50

        return _rescaled_risk

    def performance_analysis(self):

        # Category of permissions for which to calculate the performances.
        _cat = 'declared'

        # Set the seed for reproducibility purposes.
        random.seed(self.seed)

        _k_fold = StratifiedKFold(n_splits=10, shuffle=True, random_state=self.seed)

        _all_models = (SVC(kernel='linear', probability=True, random_state=self.seed),
                       GaussianNB(),
                       MultinomialNB(),
                       BernoulliNB(),
                       DecisionTreeClassifier(random_state=self.seed),
                       RandomForestClassifier(random_state=self.seed),
                       AdaBoostClassifier(random_state=self.seed),
                       GradientBoostingClassifier(random_state=self.seed),
                       SGDClassifier(loss='log', random_state=self.seed),
                       LogisticRegression(random_state=self.seed),
                       LogisticRegressionCV(random_state=self.seed),
                       KNeighborsClassifier(),
                       LinearDiscriminantAnalysis(),
                       QuadraticDiscriminantAnalysis(),
                       MLPClassifier(random_state=self.seed))

        _training_sets = list(self.get_training_vectors_3_sets())

        for model in _all_models:
            # print('\n\n\nAnalysis of ' + model.__class__.__name__ + ':')

            # Goodware and malware scores for the current model.
            _malware_scores = numpy.array([])
            _goodware_scores = numpy.array([])

            # Correctly predicted targets for the current model.
            _ok_targets = numpy.array([])

            print('\n' + r'\multirow{4}{*}{\rotatebox{90}{\parbox{3cm}{\centering \textit{' +
                  model.__class__.__name__ + r'}}\hspace{-.01\normalbaselineskip}}}')

            # We analyze the 3 training sets for each model.
            for (index, current_set) in enumerate(_training_sets):

                # current_set[0] = application set
                # current_set[1] = application targets

                # Goodware and malware scores for the current set.
                _loc_m_scores = numpy.array([])
                _loc_g_scores = numpy.array([])

                # Correctly predicted targets for the current set.
                _loc_ok_targets = numpy.array([])

                # The analysis is done using 10-cross fold validation.
                for train_index, test_index in _k_fold.split(current_set[0][_cat], current_set[1]):

                    _train_data = numpy.array(current_set[0][_cat])
                    _train_targets = numpy.array(current_set[1])

                    model.fit(_train_data[train_index], _train_targets[train_index])

                    # Correctly predicted targets for the current fold.
                    _fold_ok_targets = 0

                    for loc_index in test_index:

                        proba = list(zip(model.classes_,
                                         model.predict_proba([_train_data[loc_index]])[0]))

                        # The malware probability is considered as the risk value.
                        if proba[0][0] == 'malware':
                            _result = proba[0]
                        else:
                            _result = proba[1]

                        # We consider only correct predictions for calculating the mean
                        # and the standard deviation.
                        _true_target = _train_targets[loc_index]

                        # If the current app under test is a malware.
                        if _result[1] >= 0.5:
                            # If the prediction is correct.
                            if _result[0] == _true_target:
                                _fold_ok_targets += 1
                                _loc_m_scores = numpy.append(_loc_m_scores, _result[1])

                        # If the current app under test is not a malware.
                        else:
                            # If the prediction is correct.
                            if _result[0] != _true_target:
                                _fold_ok_targets += 1
                                _loc_g_scores = numpy.append(_loc_g_scores, _result[1])

                    _loc_ok_targets = numpy.append(_loc_ok_targets, _fold_ok_targets / len(test_index))

                # print('    set_{0}:'.format(index + 1))
                # print('        accuracy: {0:.2f}'.format(_loc_ok_targets.mean() * 100))
                # print('        malware mean: {0:.2f}'.format(_loc_m_scores.mean() * 100))
                # print('        malware std_dev: {0:.2f}'.format(_loc_m_scores.std() * 100))
                # print('        goodware mean: {0:.2f}'.format(_loc_g_scores.mean() * 100))
                # print('        goodware std_dev: {0:.2f}'.format(_loc_g_scores.std() * 100))

                print(r'& Set~$' + str(index + 1) + r'$ & $' + '{0:.2f}'.format(_loc_ok_targets.mean() * 100) +
                      r'$ & $' + '{0:.2f}'.format(_loc_m_scores.mean() * 100) + r'$ & $' +
                      '{0:.2f}'.format(_loc_m_scores.std() * 100) + r'$ & $' +
                      '{0:.2f}'.format(_loc_g_scores.mean() * 100) + r'$ & $' +
                      '{0:.2f}'.format(_loc_g_scores.std() * 100) + r'$ \\\cline{2-7}')

                _ok_targets = numpy.append(_ok_targets, _loc_ok_targets)
                _malware_scores = numpy.append(_malware_scores, _loc_m_scores)
                _goodware_scores = numpy.append(_goodware_scores, _loc_g_scores)

            # print('    total:')
            # print('        accuracy: {0:.2f}'.format(_ok_targets.mean() * 100))
            # print('        malware mean: {0:.2f}'.format(_malware_scores.mean() * 100))
            # print('        malware std_dev: {0:.2f}'.format(_malware_scores.std() * 100))
            # print('        goodware mean: {0:.2f}'.format(_goodware_scores.mean() * 100))
            # print('        goodware std_dev: {0:.2f}'.format(_goodware_scores.std() * 100))

            print(r'& Mean & $' + '{0:.2f}'.format(_ok_targets.mean() * 100) +
                  r'$ & $' + '{0:.2f}'.format(_malware_scores.mean() * 100) + r'$ & $' +
                  '{0:.2f}'.format(_malware_scores.std() * 100) + r'$ & $' +
                  '{0:.2f}'.format(_goodware_scores.mean() * 100) + r'$ & $' +
                  '{0:.2f}'.format(_goodware_scores.std() * 100) + r'$ \\\cline{2-7}')
