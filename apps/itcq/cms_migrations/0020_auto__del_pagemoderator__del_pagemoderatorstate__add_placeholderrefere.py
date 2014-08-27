# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PageModerator'
        db.delete_table(u'cms_pagemoderator')

        # Deleting model 'PageModeratorState'
        db.delete_table(u'cms_pagemoderatorstate')

        # Adding model 'PlaceholderReference'
        db.create_table(u'cms_placeholderreference', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('placeholder_ref', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True)),
        ))
        db.send_create_signal('cms', ['PlaceholderReference'])

        # Adding model 'UserSettings'
        db.create_table(u'cms_usersettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='djangocms_usersettings', unique=True, to=orm['auth.User'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('clipboard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True, blank=True)),
        ))
        db.send_create_signal('cms', ['UserSettings'])

        # Adding model 'StaticPlaceholder'
        db.create_table(u'cms_staticplaceholder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('draft', self.gf('django.db.models.fields.related.ForeignKey')(related_name='static_draft', null=True, to=orm['cms.Placeholder'])),
            ('public', self.gf('django.db.models.fields.related.ForeignKey')(related_name='static_public', null=True, to=orm['cms.Placeholder'])),
            ('dirty', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_method', self.gf('django.db.models.fields.CharField')(default='code', max_length=20, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True, blank=True)),
        ))
        db.send_create_signal('cms', ['StaticPlaceholder'])

        # Adding unique constraint on 'StaticPlaceholder', fields ['code', 'site']
        db.create_unique(u'cms_staticplaceholder', ['code', 'site_id'])

        # Adding model 'AliasPluginModel'
        db.create_table(u'cms_aliaspluginmodel', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('plugin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alias_reference', null=True, to=orm['cms.CMSPlugin'])),
            ('alias_placeholder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alias_placeholder', null=True, to=orm['cms.Placeholder'])),
        ))
        db.send_create_signal('cms', ['AliasPluginModel'])

        # Deleting field 'GlobalPagePermission.can_moderate'
        db.delete_column(u'cms_globalpagepermission', 'can_moderate')

        # Deleting field 'PagePermission.can_moderate'
        db.delete_column(u'cms_pagepermission', 'can_moderate')

        # Deleting field 'Title.meta_keywords'
        db.delete_column(u'cms_title', 'meta_keywords')

        # Deleting field 'Title.application_urls'
        db.delete_column(u'cms_title', 'application_urls')

        # Adding field 'Title.published'
        db.add_column(u'cms_title', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Title.publisher_is_draft'
        db.add_column(u'cms_title', 'publisher_is_draft',
                      self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True),
                      keep_default=False)

        # Adding field 'Title.publisher_public'
        db.add_column(u'cms_title', 'publisher_public',
                      self.gf('django.db.models.fields.related.OneToOneField')(related_name='publisher_draft', unique=True, null=True, to=orm['cms.Title']),
                      keep_default=False)

        # Adding field 'Title.publisher_state'
        db.add_column(u'cms_title', 'publisher_state',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0, db_index=True),
                      keep_default=False)


        # Changing field 'Title.meta_description'
        db.alter_column(u'cms_title', 'meta_description', self.gf('django.db.models.fields.TextField')(max_length=155, null=True))
        # Deleting field 'Page.moderator_state'
        print 'delete page moderator state'
        db.delete_column(u'cms_page', 'moderator_state')

        # Deleting field 'Page.publisher_state'
        db.delete_column(u'cms_page', 'publisher_state')

        # Deleting field 'Page.published'
        db.delete_column(u'cms_page', 'published')

        # Adding field 'Page.is_home'
        db.add_column(u'cms_page', 'is_home',
                      self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True),
                      keep_default=False)

        # Adding field 'Page.application_urls'
        db.add_column(u'cms_page', 'application_urls',
                      self.gf('django.db.models.fields.CharField')(db_index=True, max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.application_namespace'
        db.add_column(u'cms_page', 'application_namespace',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.languages'
        db.add_column(u'cms_page', 'languages',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.revision_id'
        db.add_column(u'cms_page', 'revision_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Page.xframe_options'
        db.add_column(u'cms_page', 'xframe_options',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding unique constraint on 'Page', fields ['reverse_id', 'site', 'publisher_is_draft']
        db.create_unique(u'cms_page', ['reverse_id', 'site_id', 'publisher_is_draft'])

        # Adding unique constraint on 'Page', fields ['publisher_is_draft', 'application_namespace']
        db.create_unique(u'cms_page', ['publisher_is_draft', 'application_namespace'])


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['publisher_is_draft', 'application_namespace']
        db.delete_unique(u'cms_page', ['publisher_is_draft', 'application_namespace'])

        # Removing unique constraint on 'Page', fields ['reverse_id', 'site', 'publisher_is_draft']
        db.delete_unique(u'cms_page', ['reverse_id', 'site_id', 'publisher_is_draft'])

        # Removing unique constraint on 'StaticPlaceholder', fields ['code', 'site']
        db.delete_unique(u'cms_staticplaceholder', ['code', 'site_id'])

        # Adding model 'PageModerator'
        db.create_table(u'cms_pagemoderator', (
            ('moderate_children', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('moderate_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('moderate_descendants', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('cms', ['PageModerator'])

        # Adding model 'PageModeratorState'
        db.create_table(u'cms_pagemoderatorstate', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(default='', max_length=1000, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cms', ['PageModeratorState'])

        # Deleting model 'PlaceholderReference'
        db.delete_table(u'cms_placeholderreference')

        # Deleting model 'UserSettings'
        db.delete_table(u'cms_usersettings')

        # Deleting model 'StaticPlaceholder'
        db.delete_table(u'cms_staticplaceholder')

        # Deleting model 'AliasPluginModel'
        db.delete_table(u'cms_aliaspluginmodel')

        # Adding field 'GlobalPagePermission.can_moderate'
        db.add_column(u'cms_globalpagepermission', 'can_moderate',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'PagePermission.can_moderate'
        db.add_column(u'cms_pagepermission', 'can_moderate',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Title.meta_keywords'
        db.add_column(u'cms_title', 'meta_keywords',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Title.application_urls'
        db.add_column(u'cms_title', 'application_urls',
                      self.gf('django.db.models.fields.CharField')(blank=True, max_length=200, null=True, db_index=True),
                      keep_default=False)

        # Deleting field 'Title.published'
        db.delete_column(u'cms_title', 'published')

        # Deleting field 'Title.publisher_is_draft'
        db.delete_column(u'cms_title', 'publisher_is_draft')

        # Deleting field 'Title.publisher_public'
        db.delete_column(u'cms_title', 'publisher_public_id')

        # Deleting field 'Title.publisher_state'
        db.delete_column(u'cms_title', 'publisher_state')


        # Changing field 'Title.meta_description'
        db.alter_column(u'cms_title', 'meta_description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))
        # Adding field 'Page.moderator_state'
        print 'add page moderator state'
        db.add_column(u'cms_page', 'moderator_state',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1, blank=True),
                      keep_default=False)

        # Adding field 'Page.publisher_state'
        db.add_column(u'cms_page', 'publisher_state',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'Page.published'
        db.add_column(u'cms_page', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Page.is_home'
        db.delete_column(u'cms_page', 'is_home')

        # Deleting field 'Page.application_urls'
        db.delete_column(u'cms_page', 'application_urls')

        # Deleting field 'Page.application_namespace'
        db.delete_column(u'cms_page', 'application_namespace')

        # Deleting field 'Page.languages'
        db.delete_column(u'cms_page', 'languages')

        # Deleting field 'Page.revision_id'
        db.delete_column(u'cms_page', 'revision_id')

        # Deleting field 'Page.xframe_options'
        db.delete_column(u'cms_page', 'xframe_options')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cms.aliaspluginmodel': {
            'Meta': {'object_name': 'AliasPluginModel', '_ormbases': ['cms.CMSPlugin']},
            'alias_placeholder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alias_placeholder'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alias_reference'", 'null': 'True', 'to': "orm['cms.CMSPlugin']"})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.globalpagepermission': {
            'Meta': {'object_name': 'GlobalPagePermission'},
            'can_add': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_change': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_change_advanced_settings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_change_permissions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_delete': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_move_page': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_recover_page': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'cms.page': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('publisher_is_draft', 'application_namespace'), ('reverse_id', 'site', 'publisher_is_draft'))", 'object_name': 'Page'},
            'application_namespace': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'application_urls': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'changed_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_home': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'limit_visibility_in_menu': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'navigation_extenders': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cms.Page']"}),
            'placeholders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cms.Placeholder']", 'symmetrical': 'False'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.Page']"}),
            'reverse_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'revision_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'djangocms_pages'", 'to': u"orm['sites.Site']"}),
            'soft_root': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'INHERIT'", 'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'xframe_options': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'cms.pagepermission': {
            'Meta': {'object_name': 'PagePermission'},
            'can_add': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_change': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_change_advanced_settings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_change_permissions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_delete': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_move_page': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_view': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grant_on': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'cms.pageuser': {
            'Meta': {'object_name': 'PageUser', '_ormbases': [u'auth.User']},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_users'", 'to': u"orm['auth.User']"}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'cms.pageusergroup': {
            'Meta': {'object_name': 'PageUserGroup', '_ormbases': [u'auth.Group']},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_usergroups'", 'to': u"orm['auth.User']"}),
            u'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'primary_key': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cms.placeholderreference': {
            'Meta': {'object_name': 'PlaceholderReference', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'placeholder_ref': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'})
        },
        'cms.staticplaceholder': {
            'Meta': {'unique_together': "(('code', 'site'),)", 'object_name': 'StaticPlaceholder'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'creation_method': ('django.db.models.fields.CharField', [], {'default': "'code'", 'max_length': '20', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'static_draft'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'public': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'static_public'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'})
        },
        'cms.title': {
            'Meta': {'unique_together': "(('language', 'page'),)", 'object_name': 'Title'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'has_url_overwrite': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'menu_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'max_length': '155', 'null': 'True', 'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'title_set'", 'to': "orm['cms.Page']"}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.Title']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'redirect': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cms.usersettings': {
            'Meta': {'object_name': 'UserSettings'},
            'clipboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'djangocms_usersettings'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cms']
