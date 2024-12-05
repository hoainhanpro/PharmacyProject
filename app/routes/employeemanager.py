from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.database import create_connection, execute_query